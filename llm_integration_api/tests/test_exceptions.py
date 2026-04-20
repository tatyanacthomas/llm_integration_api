import pytest

from llm_integration_api.exceptions import (
	AuthenticationError,
	AuthorizationError,
	ClientError,
	ConflictError,
	LLMIntegrationError,
	MessageError,
	MessageNotFound,
	MessageValidationError,
	NotFoundError,
	RequestError,
	ResponseError,
	ResponseNotFoundError,
	ResponseValidationError,
	ValidationError,
)


def test_llm_integration_error_stores_provider_and_cause():
	cause = ValueError("bad value")
	err = LLMIntegrationError("top level", provider="openai", cause=cause)

	assert str(err) == "top level"
	assert err.provider == "openai"
	assert err.cause is cause


@pytest.mark.parametrize(
	"exc_type,parent_type",
	[
		(ValidationError, LLMIntegrationError),
		(RequestError, LLMIntegrationError),
		(NotFoundError, RequestError),
		(ConflictError, RequestError),
		(AuthenticationError, LLMIntegrationError),
		(AuthorizationError, LLMIntegrationError),
		(ClientError, LLMIntegrationError),
		(MessageError, LLMIntegrationError),
		(ResponseError, LLMIntegrationError),
	],
)
def test_exception_inheritance_tree(exc_type, parent_type):
	assert issubclass(exc_type, parent_type)


def test_message_not_found_multiple_inheritance():
	assert issubclass(MessageNotFound, MessageError)
	assert issubclass(MessageNotFound, NotFoundError)


def test_message_validation_multiple_inheritance():
	assert issubclass(MessageValidationError, MessageError)
	assert issubclass(MessageValidationError, ValidationError)


def test_response_not_found_multiple_inheritance():
	assert issubclass(ResponseNotFoundError, ResponseError)
	assert issubclass(ResponseNotFoundError, NotFoundError)


def test_response_validation_multiple_inheritance():
	assert issubclass(ResponseValidationError, ResponseError)
	assert issubclass(ResponseValidationError, ValidationError)
