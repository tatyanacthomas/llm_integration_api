import pytest
import requests

from llm_integration_api.interface import exceptions as interface_exceptions

from llm_integration_api.open_router_impl.open_router_client import OpenRouterClient
from llm_integration_api.open_router_impl.open_router_message import OpenRouterMessage


def _raw_response(content: str = "hi", prompt_tokens: int = 3, completion_tokens: int = 4) -> dict:
    return {
        "choices": [{"message": {"content": content}}],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
        },
    }


def test_open_router_client_constructor_validates_required_fields() -> None:
    with pytest.raises(interface_exceptions.AuthenticationError):
        OpenRouterClient(api_key="", model="openai/gpt-4o")

    with pytest.raises(interface_exceptions.ClientError):
        OpenRouterClient(api_key="test-key", model="")


def test_open_router_client_properties_and_get_message_error() -> None:
    client = OpenRouterClient(api_key="test-key", model="openai/gpt-4o")

    assert client.provider == "openrouter"
    assert client.api_key == "test-key"
    assert client.model == "openai/gpt-4o"

    with pytest.raises(interface_exceptions.MessageError):
        client.get_message()


def test_open_router_client_requires_response_for_helpers() -> None:
    client = OpenRouterClient(api_key="test-key", model="openai/gpt-4o")

    with pytest.raises(interface_exceptions.ResponseError):
        client.get_response()
    with pytest.raises(interface_exceptions.ResponseError):
        client.display_response()
    with pytest.raises(interface_exceptions.ResponseError):
        client.total_tokens()


def test_open_router_client_send_message_success(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    captured: dict = {}

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return _raw_response(content="Hello back", prompt_tokens=11, completion_tokens=9)

    def fake_post(url: str, json: dict, headers: dict, timeout: int):
        captured["url"] = url
        captured["json"] = json
        captured["headers"] = headers
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(requests, "post", fake_post)

    client = OpenRouterClient(
        api_key="test-key",
        model="openai/gpt-4o",
        site_url="https://example.com",
        app_name="my-app",
    )
    history = [
        OpenRouterMessage(role="system", content="You are concise."),
        OpenRouterMessage(role="user", content="Say hi"),
    ]

    response = client.send_message(history)

    assert response.content == "Hello back"
    assert captured["url"] == OpenRouterClient.BASE_URL
    assert captured["json"] == {
        "model": "openai/gpt-4o",
        "messages": [
            {"role": "system", "content": "You are concise."},
            {"role": "user", "content": "Say hi"},
        ],
    }
    assert captured["headers"]["Authorization"] == "Bearer test-key"
    assert captured["headers"]["HTTP-Referer"] == "https://example.com"
    assert captured["headers"]["X-Title"] == "my-app"
    assert captured["timeout"] == 60

    assert client.total_tokens() == 20
    assert client.get_response() == {
        "content": "Hello back",
        "prompt_tokens": 11,
        "completion_tokens": 9,
        "total_tokens": 20,
    }

    client.display_response()
    output = capsys.readouterr().out
    assert "[openrouter / openai/gpt-4o]" in output
    assert "Hello back" in output
    assert "total: 20" in output


def test_open_router_client_send_message_rejects_empty_history() -> None:
    client = OpenRouterClient(api_key="test-key", model="openai/gpt-4o")

    with pytest.raises(interface_exceptions.MessageValidationError):
        client.send_message([])


def test_open_router_client_maps_http_401_to_authentication_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeResponse:
        status_code = 401

        def raise_for_status(self) -> None:
            raise requests.HTTPError("unauthorized", response=self)

    monkeypatch.setattr(requests, "post", lambda *args, **kwargs: FakeResponse())

    client = OpenRouterClient(api_key="bad-key", model="openai/gpt-4o")
    history = [OpenRouterMessage(role="user", content="Hi")]

    with pytest.raises(interface_exceptions.AuthenticationError) as exc_info:
        client.send_message(history)

    assert exc_info.value.provider == "openrouter"
    assert exc_info.value.cause is not None


def test_open_router_client_maps_other_http_errors_to_client_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeResponse:
        status_code = 500

        def raise_for_status(self) -> None:
            raise requests.HTTPError("server error", response=self)

    monkeypatch.setattr(requests, "post", lambda *args, **kwargs: FakeResponse())

    client = OpenRouterClient(api_key="test-key", model="openai/gpt-4o")
    history = [OpenRouterMessage(role="user", content="Hi")]

    with pytest.raises(interface_exceptions.ClientError) as exc_info:
        client.send_message(history)

    assert "HTTP 500" in str(exc_info.value)
    assert exc_info.value.provider == "openrouter"
    assert exc_info.value.cause is not None


def test_open_router_client_maps_request_exception_to_client_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_post(*args, **kwargs):
        raise requests.RequestException("connection dropped")

    monkeypatch.setattr(requests, "post", fake_post)

    client = OpenRouterClient(api_key="test-key", model="openai/gpt-4o")
    history = [OpenRouterMessage(role="user", content="Hi")]

    with pytest.raises(interface_exceptions.ClientError) as exc_info:
        client.send_message(history)

    assert "Network error contacting OpenRouter" in str(exc_info.value)
    assert exc_info.value.provider == "openrouter"
    assert exc_info.value.cause is not None
