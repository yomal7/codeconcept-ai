from google.genai import errors as google_errors


def is_rate_limit(exc: Exception | None) -> bool:
    """True if exc is Gemini telling us to slow down (429 / quota / resource exhausted).

    Shared by GeminiClient and GeminiTTSClient.
    """
    if isinstance(exc, google_errors.ClientError):
        message = str(exc).lower()
        return getattr(exc, "code", None) == 429 or "resource_exhausted" in message or "quota" in message
    return False