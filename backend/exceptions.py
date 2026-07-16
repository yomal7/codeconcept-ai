class LLMError(Exception):
    """Base class for all LLM-related failures. Catch this if you just
    want to know "something went wrong talking to the model"."""


class LLMRateLimitError(LLMError):
    """The provider is temporarily rate-limited or out of quota."""


class LLMGenerationError(LLMError):
    """The provider failed to produce a response at all."""


class LLMValidationError(LLMError):
    """The provider responded, but the output didn't match the requested schema."""