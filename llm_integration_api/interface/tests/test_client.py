import pytest

from llm_integration_api.interface.client import Client


class DummyClient(Client):
    def __init__(self):
        self._provider = "openai"
        self._api_key = "test-key"
        self._model = "gpt-test"
        self.prompt_tokens = 12
        self.completion_tokens = 8

    @property
    def provider(self) -> str:
        return self._provider

    @property
    def api_key(self) -> str:
        return self._api_key

    @property
    def model(self) -> str:
        return self._model

    def get_message(self) -> dict:
        return {"role": "user", "content": "Hello"}

    def send_message(self, history: list):
        history.append(self.get_message())
        return {"content": "Hi there"}

    def get_response(self) -> dict:
        return {
            "content": "Hi there",
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
        }

    def display_response(self) -> None:
        return None


def test_client_concrete_implementation_behaves_as_expected():
    client = DummyClient()

    assert client.provider == "openai"
    assert client.api_key == "test-key"
    assert client.model == "gpt-test"
    assert client.get_message() == {"role": "user", "content": "Hello"}

    history = []
    result = client.send_message(history)
    assert history == [{"role": "user", "content": "Hello"}]
    assert result == {"content": "Hi there"}

    assert client.get_response() == {
        "content": "Hi there",
        "prompt_tokens": 12,
        "completion_tokens": 8,
    }


def test_client_total_tokens_returns_sum():
    client = DummyClient()

    assert client.total_tokens() == 20


def test_client_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        Client()


def test_client_with_missing_abstract_member_is_not_instantiable():
    class IncompleteClient(Client):
        @property
        def provider(self) -> str:
            return "openai"

        @property
        def api_key(self) -> str:
            return "key"

        @property
        def model(self) -> str:
            return "model"

        def get_message(self) -> dict:
            return {"role": "user", "content": "x"}

        def send_message(self, history: list):
            return {}

        def get_response(self) -> dict:
            return {}

    with pytest.raises(TypeError):
        IncompleteClient()
