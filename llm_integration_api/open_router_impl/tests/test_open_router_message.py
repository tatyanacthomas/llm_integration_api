import pytest

from llm_integration_api.interface import exceptions as interface_exceptions

from llm_integration_api.open_router_impl.open_router_message import OpenRouterMessage


def test_open_router_message_accepts_valid_inputs() -> None:
    msg = OpenRouterMessage(role="user", content="Hello")

    assert msg.role == "user"
    assert msg.content == "Hello"


@pytest.mark.parametrize("role", ["", "tool", "USER", "developer"])
def test_open_router_message_rejects_invalid_role(role: str) -> None:
    with pytest.raises(interface_exceptions.MessageValidationError) as exc_info:
        OpenRouterMessage(role=role, content="Hello")

    assert "Invalid role" in str(exc_info.value)
    assert exc_info.value.provider == "openrouter"


@pytest.mark.parametrize("content", ["", "   ", "\n\t"])
def test_open_router_message_rejects_blank_content(content: str) -> None:
    with pytest.raises(interface_exceptions.MessageValidationError) as exc_info:
        OpenRouterMessage(role="user", content=content)

    assert "must not be empty" in str(exc_info.value)
    assert exc_info.value.provider == "openrouter"
