class LLMError(Exception):
    """Base error for a model request."""


class LLMUnreachableError(LLMError):
    """The model server could not be reached."""


class LLMModelNotFoundError(LLMError):
    """The requested model is not available on the server."""


class LLMTimeoutError(LLMError):
    """The model server did not answer in time."""
