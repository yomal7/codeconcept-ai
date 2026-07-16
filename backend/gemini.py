import json
import time
from typing import TypeVar

from google import genai
from google.genai import errors as google_errors
from pydantic import BaseModel

from backend.exceptions import LLMGenerationError, LLMRateLimitError, LLMValidationError
from backend.llm_client import LLMClient
from config.settings import GEMINI_MODEL, GOOGLE_API_KEY

T = TypeVar("T", bound=BaseModel)


class GeminiClient(LLMClient):
    """Google Gemini implementation of the LLMClient contract.

    Every Gemini-specific quirk (schema field stripping, rate-limit
    detection, retry/backoff) lives in this one file. Agents never see
    any of it.
    """

    def __init__(self):
        self._client = genai.Client(api_key=GOOGLE_API_KEY)
        self.client = self._client

    def generate_text(self, prompt: str, *, model: str | None = None) -> str:
        response = self._call(prompt, model=model, config=None)
        return response.text or ""

    def generate(self, prompt: str, *, model: str | None = None, response_schema=None, retries: int = 3, delay_seconds: float = 2.0):
        if response_schema is None:
            return self.generate_text(prompt, model=model)
        return self.generate_structured(prompt, response_schema, model=model)

    def generate_structured(self, prompt: str, schema: type[T], *, model: str | None = None) -> T:
        config = {
            "response_mime_type": "application/json",
            "response_schema": self._to_gemini_schema(schema),
        }
        response = self._call(prompt, model=model, config=config)
        return self._parse(response, schema)

    # ---- internals ---------------------------------------------------

    def _call(self, prompt: str, *, model, config, retries: int = 3, delay_seconds: float = 2.0):
        selected_model = model or GEMINI_MODEL
        last_error: Exception | None = None

        client = getattr(self, "_client", None) or getattr(self, "client", None)
        if client is None:
            raise LLMGenerationError("Gemini client is not initialized")

        for attempt in range(retries):
            try:
                return client.models.generate_content(
                    model=selected_model,
                    contents=prompt,
                    config=config,
                )
            except Exception as exc:
                last_error = exc
                if self._is_rate_limit(exc) and attempt < retries - 1:
                    time.sleep(delay_seconds * (attempt + 1))
                    continue
                break

        if self._is_rate_limit(last_error):
            raise LLMRateLimitError("Gemini is temporarily rate-limited. Please retry shortly.") from last_error
        raise LLMGenerationError(f"Gemini generation failed: {last_error}") from last_error

    def _parse(self, response, schema: type[T]) -> T:
        parsed = getattr(response, "parsed", None)
        if isinstance(parsed, schema):
            return parsed
        if isinstance(parsed, dict):
            return self._validate(parsed, schema)

        text = getattr(response, "text", None)
        if not text:
            raise LLMValidationError("Gemini returned no content for the requested schema")

        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise LLMValidationError("Gemini returned invalid JSON") from exc

        return self._validate(data, schema)

    def _validate(self, data: dict, schema: type[T]) -> T:
        try:
            return schema.model_validate(data)
        except Exception as exc:
            raise LLMValidationError(
                f"Gemini response did not match the {schema.__name__} schema"
            ) from exc

    def build_response_schema(self, schema: type[BaseModel]) -> dict:
        return self._strip_unsupported_fields(schema.model_json_schema())

    def _to_gemini_schema(self, schema: type[BaseModel]) -> dict:
        return self.build_response_schema(schema)

    def _strip_unsupported_fields(self, node):
        if isinstance(node, dict):
            cleaned = {}
            for key, value in node.items():
                if key in {"additionalProperties", "exclusiveMinimum", "exclusiveMaximum"}:
                    continue
                cleaned[key] = self._strip_unsupported_fields(value)
            return cleaned
        if isinstance(node, list):
            return [self._strip_unsupported_fields(item) for item in node]
        return node

    def _is_rate_limit(self, exc: Exception | None) -> bool:
        if isinstance(exc, google_errors.ClientError):
            message = str(exc).lower()
            return getattr(exc, "code", None) == 429 or "resource_exhausted" in message or "quota" in message
        return False