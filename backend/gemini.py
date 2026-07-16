import json
import time

from google import genai
from google.genai import errors as google_errors

from backend.exceptions import GeminiRateLimitError, InvalidPresentationError
from backend.models import Presentation
from config.settings import GEMINI_MODEL, GOOGLE_API_KEY


class GeminiClient:

    def __init__(self):

        self.client = genai.Client(
            api_key=GOOGLE_API_KEY
        )

    def build_response_schema(self, response_schema):
        schema = response_schema.model_json_schema()
        return self._strip_unsupported_schema_fields(schema)

    def _strip_unsupported_schema_fields(self, schema):
        if isinstance(schema, dict):
            cleaned = {}
            for key, value in schema.items():
                if key == "additionalProperties":
                    continue
                if isinstance(value, list):
                    cleaned[key] = [self._strip_unsupported_schema_fields(item) for item in value]
                elif isinstance(value, dict):
                    cleaned[key] = self._strip_unsupported_schema_fields(value)
                else:
                    cleaned[key] = value
            return cleaned
        if isinstance(schema, list):
            return [self._strip_unsupported_schema_fields(item) for item in schema]
        return schema

    def _is_rate_limit_error(self, exc: Exception) -> bool:
        if isinstance(exc, google_errors.ClientError):
            status_code = getattr(exc, "code", None)
            message = str(exc).lower()
            return status_code == 429 or "resource_exhausted" in message or "quota" in message
        return False

    def generate(
        self,
        prompt: str,
        model: str | None = None,
        response_schema=None,
        retries: int = 3,
        delay_seconds: float = 2.0,
    ):

        config = None
        if response_schema is not None:
            config = {
                "response_mime_type": "application/json",
                "response_schema": self.build_response_schema(response_schema),
            }

        selected_model = model or GEMINI_MODEL

        last_error = None
        response = None
        for attempt in range(retries):
            try:
                response = self.client.models.generate_content(
                    model=selected_model,
                    contents=prompt,
                    config=config,
                )
                break
            except Exception as exc:
                last_error = exc
                if self._is_rate_limit_error(exc) and attempt < retries - 1:
                    time.sleep(delay_seconds * (attempt + 1))
                    continue
                raise

        if response is None:
            if self._is_rate_limit_error(last_error):
                raise GeminiRateLimitError(
                    "Gemini API is temporarily rate-limited. Please retry shortly."
                ) from last_error
            raise InvalidPresentationError(f"Gemini generation failed: {last_error}") from last_error

        if response_schema is None:
            return response.text

        if getattr(response, "parsed", None) is not None:
            parsed = response.parsed
            if isinstance(parsed, response_schema):
                return parsed
            if isinstance(parsed, dict):
                try:
                    return response_schema.model_validate(parsed)
                except Exception as exc:
                    raise InvalidPresentationError(
                        "Gemini response did not match the presentation schema"
                    ) from exc

        text = getattr(response, "text", None)
        if not text:
            raise InvalidPresentationError("Gemini returned no content for the requested schema")

        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise InvalidPresentationError("Gemini returned invalid JSON") from exc

        try:
            return response_schema.model_validate(data)
        except Exception as exc:
            raise InvalidPresentationError(
                "Gemini response did not match the presentation schema"
            ) from exc