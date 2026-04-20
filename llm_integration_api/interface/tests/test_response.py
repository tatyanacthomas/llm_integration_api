import pytest

from llm_integration_api.interface.response import Response


class DummyResponse(Response):
    def __init__(self, content: str, prompt_tokens: int, completion_tokens: int):
        self._content = content
        self._prompt_tokens = prompt_tokens
        self._completion_tokens = completion_tokens

    @property
    def content(self) -> str:
        return self._content

    @property
    def prompt_tokens(self) -> int:
        return self._prompt_tokens

    @property
    def completion_tokens(self) -> int:
        return self._completion_tokens


def test_response_constructor_and_properties():
    response = DummyResponse(content="Hello", prompt_tokens=7, completion_tokens=3)

    assert response.content == "Hello"
    assert response.prompt_tokens == 7
    assert response.completion_tokens == 3


def test_response_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        Response()


def test_response_with_missing_abstract_property_is_not_instantiable():
    class IncompleteResponse(Response):
        @property
        def content(self) -> str:
            return self._content

        @property
        def prompt_tokens(self) -> int:
            return self._prompt_tokens

    with pytest.raises(TypeError):
        IncompleteResponse()
