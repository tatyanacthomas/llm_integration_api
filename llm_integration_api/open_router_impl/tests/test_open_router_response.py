import pytest

from llm_integration_api.interface import exceptions as interface_exceptions

from llm_integration_api.open_router_impl.open_router_response import OpenRouterResponse


def test_open_router_response_parses_valid_payload() -> None:
    raw = {
        "choices": [{"message": {"content": "Hello from model"}}],
        "usage": {"prompt_tokens": 5, "completion_tokens": 7},
    }

    response = OpenRouterResponse(raw)

    assert response.content == "Hello from model"
    assert response.prompt_tokens == 5
    assert response.completion_tokens == 7


@pytest.mark.parametrize(
    "raw",
    [
        {},
        {"choices": [], "usage": {"prompt_tokens": 1, "completion_tokens": 2}},
        {"choices": [{}], "usage": {"prompt_tokens": 1, "completion_tokens": 2}},
        {"choices": [{"message": {"content": "x"}}]},
    ],
)
def test_open_router_response_rejects_unexpected_structure(raw: dict) -> None:
    with pytest.raises(interface_exceptions.ResponseValidationError) as exc_info:
        OpenRouterResponse(raw)

    assert "Unexpected OpenRouter response structure" in str(exc_info.value)
    assert exc_info.value.provider == "openrouter"
    assert exc_info.value.cause is not None
