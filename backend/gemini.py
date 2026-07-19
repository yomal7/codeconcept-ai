import json
from typing import TypeVar

from google import genai
from pydantic import BaseModel

from backend.exceptions import LLMGenerationError, LLMRateLimitError, LLMValidationError
from backend.gemini_errors import is_rate_limit
from backend.llm_client import LLMClient
from backend.retry import call_with_retry
from config.settings import GEMINI_MODEL, GOOGLE_API_KEY

T = TypeVar("T", bound=BaseModel)


class GeminiClient(LLMClient):
    """Google Gemini implementation of the LLMClient contract.

    Every Gemini-specific quirk (schema field stripping, response parsing)
    lives in this one file. Retry/backoff and rate-limit detection are
    shared with GeminiTTSClient via backend/retry.py and
    backend/gemini_errors.py instead of being duplicated here.
    """

    def __init__(self):
        self._client = genai.Client(api_key=GOOGLE_API_KEY)

    def generate_text(self, prompt: str, *, model: str | None = None) -> str:
        response = self._call(prompt, model=model, config=None)
        return response.text or ""

    def generate_structured(self, prompt: str, schema: type[T], *, model: str | None = None) -> T:
        config = {
            "response_mime_type": "application/json",
            "response_schema": self._to_gemini_schema(schema),
        }
        response = self._call(prompt, model=model, config=config)
        return self._parse(response, schema)

    # ---- internals ---------------------------------------------------

    def _call(self, prompt: str, *, model, config):
        selected_model = model or GEMINI_MODEL
        try:
            return call_with_retry(
                lambda: self._client.models.generate_content(
                    model=selected_model,
                    contents=prompt,
                    config=config,
                ),
                is_retryable=is_rate_limit,
            )
        except Exception as exc:
            if is_rate_limit(exc):
                raise LLMRateLimitError("Gemini is temporarily rate-limited. Please retry shortly.") from exc
            raise LLMGenerationError(f"Gemini generation failed: {exc}") from exc

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

    def _to_gemini_schema(self, schema: type[BaseModel]) -> dict:
        return self._strip_unsupported_fields(schema.model_json_schema())

    def _strip_unsupported_fields(self, node):
        if isinstance(node, dict):
            return {
                key: self._strip_unsupported_fields(value)
                for key, value in node.items()
                if key != "additionalProperties"
            }
        if isinstance(node, list):
            return [self._strip_unsupported_fields(item) for item in node]
        return node