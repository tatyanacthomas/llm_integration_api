from llm_integration_api.interface.response import Response
from llm_integration_api.interface.exceptions import ResponseValidationError


class OpenRouterResponse(Response):
    """Concrete Response implementation wrapping an OpenRouter API response."""

    def __init__(self, raw: dict) -> None:
        try:
            choice = raw["choices"][0]
            self._content = choice["message"]["content"]
            usage = raw["usage"]
            self._prompt_tokens = usage["prompt_tokens"]
            self._completion_tokens = usage["completion_tokens"]
        except (KeyError, IndexError) as exc:
            raise ResponseValidationError(
                f"Unexpected OpenRouter response structure: {exc}",
                provider="openrouter",
                cause=exc,
            )

    @property
    def content(self) -> str:
        return self._content

    @property
    def prompt_tokens(self) -> int:
        return self._prompt_tokens

    @property
    def completion_tokens(self) -> int:
        return self._completion_tokens