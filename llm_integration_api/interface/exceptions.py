"""Exception hierarchy for the LLM Integration API.

Hierarchy:
    LLMIntegrationError
    |- ValidationError
    |- RequestError
    |  |- NotFoundError
    |  |- ConflictError
    |- AuthenticationError
    |- AuthorizationError
    |- MessageError
    |  |- MessageNotFound (MessageError, NotFoundError)
    |  |- MessageValidationError (MessageError, ValidationError)
    |- ResponseErrow
       |- ResponseNotFoundError (ResponseError, NotFoundError)
       |- ResponseValidationError (ResponseError, ValidationError)

"""

class LLMIntegrationError(Exception):
    """Base exception for all LLM Integration API errors."""

    def __init__(
        self,
        message: str,
        *,
        provider: str | None = None,
        cause: Exception | None = None,
    ):
        super().__init__(message)
        self.provider = provider
        self.cause = cause

class ValidationError(LLMIntegrationError):
    """Input payload/parameters are invalid before sending to provider."""

class RequestError(LLMIntegrationError):
    """Generic remote request failure."""

class NotFoundError(RequestError):
    """Requested resource was not found in the provider."""

class ConflictError(RequestError):
    """Requested operation conflicts with current provider state."""

#Authentication-specific exceptions -------------------------------------------------------
class AuthenticationError(LLMIntegrationError):
    """Authentication failed (invalid token, expired credentials)."""

class AuthorizationError(LLMIntegrationError):
    """Authenticated but not allowed to perform action."""


class ClientError(LLMIntegrationError):
    """Base class for client-specific errors."""

#Message-specific exceptions ----------------------------------------------------------------

class MessageError(LLMIntegrationError):
    """Base class for mesage-specific errors."""

class MessageNotFound(MessageError, NotFoundError):
    """Raised when an message ID cannot be found."""

class MessageValidationError(MessageError, ValidationError):
    """Raised when message input fails validation."""

# Response-specific exceptions -------------------------------------------------------------

class ResponseError(LLMIntegrationError):
    """Base class for response-specific errors."""

class ResponseNotFoundError(ResponseError, NotFoundError):
    """Raised when a response ID cannot be found."""

class ResponseValidationError(ResponseError, ValidationError):
    """Raised when response input fails validation."""

