class InvalidPresentationError(Exception):
    """Raised when the AI generates an invalid presentation."""


class GeminiRateLimitError(Exception):
    """Raised when the Gemini API is temporarily rate-limited."""
