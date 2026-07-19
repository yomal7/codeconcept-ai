class LLMError(Exception):
    """Base class for all LLM-related failures."""


class LLMRateLimitError(LLMError):
    """The provider is temporarily rate-limited or out of quota."""


class LLMGenerationError(LLMError):
    """The provider failed to produce a response at all."""


class LLMValidationError(LLMError):
    """The provider responded, but the output didn't match the requested schema."""


class RenderError(Exception):
    """Raised when the HTML -> PNG -> MP4 rendering pipeline fails
    (Puppeteer, ffmpeg, or any other subprocess step)."""