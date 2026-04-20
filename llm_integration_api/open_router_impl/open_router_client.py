import requests

from llm_integration_api.interface.client import Client
from llm_integration_api.interface.exceptions import (
    AuthenticationError,
    ClientError,
    MessageError,
    MessageValidationError,
    ResponseError,
)
from .open_router_message import OpenRouterMessage
from .open_router_response import OpenRouterResponse


class OpenRouterClient(Client):
    """Concrete Client implementation for the OpenRouter API.

    Args:
        api_key:  Your OpenRouter API key (https://openrouter.ai/keys).
        model:    Any model slug supported by OpenRouter,
                  e.g. "openai/gpt-4o", "anthropic/claude-3.5-sonnet".
        site_url: Optional — forwarded as HTTP-Referer (OpenRouter best practice).
        app_name: Optional — forwarded as X-Title.
    """

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(
        self,
        api_key: str,
        model: str,
        site_url: str = "",
        app_name: str = "",
    ) -> None:
        if not api_key:
            raise AuthenticationError(
                "api_key must not be empty.", provider="openrouter"
            )
        if not model:
            raise ClientError("model must not be empty.", provider="openrouter")

        self._api_key = api_key
        self._model = model
        self._site_url = site_url
        self._app_name = app_name
        self._last_response: OpenRouterResponse | None = None

    # -- Client properties --------------------------------------------------

    @property
    def provider(self) -> str:
        return "openrouter"

    @property
    def api_key(self) -> str:
        return self._api_key

    @property
    def model(self) -> str:
        return self._model

    # -- Message methods ----------------------------------------------------

    def get_message(self) -> dict:
        raise MessageError(
            "Use OpenRouterMessage(role, content) to build message dicts; "
            "OpenRouterClient.get_message() is not applicable.",
            provider="openrouter",
        )

    def send_message(self, history: list[OpenRouterMessage]) -> OpenRouterResponse:
        """Send a conversation history to OpenRouter and return a Response.

        Args:
            history: Ordered list of OpenRouterMessage objects representing
                     the full conversation so far.
        """
        if not history:
            raise MessageValidationError(
                "history must contain at least one message.", provider="openrouter"
            )

        payload = {
            "model": self._model,
            "messages": [{"role": m.role, "content": m.content} for m in history],
        }

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        if self._site_url:
            headers["HTTP-Referer"] = self._site_url
        if self._app_name:
            headers["X-Title"] = self._app_name

        try:
            resp = requests.post(self.BASE_URL, json=payload, headers=headers, timeout=60)
            resp.raise_for_status()
        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else None
            if status == 401:
                raise AuthenticationError(
                    "OpenRouter rejected the API key.", provider="openrouter", cause=exc
                )
            raise ClientError(
                f"OpenRouter request failed (HTTP {status}).", provider="openrouter", cause=exc
            )
        except requests.RequestException as exc:
            raise ClientError(
                f"Network error contacting OpenRouter: {exc}", provider="openrouter", cause=exc
            )

        self._last_response = OpenRouterResponse(resp.json())
        return self._last_response

    # -- Response methods ---------------------------------------------------

    def get_response(self) -> dict:
        """Return the last response as a plain dict."""
        self._require_response()
        r = self._last_response
        return {
            "content": r.content,
            "prompt_tokens": r.prompt_tokens,
            "completion_tokens": r.completion_tokens,
            "total_tokens": self.total_tokens(),
        }

    def display_response(self) -> None:
        """Print the last response to stdout in a readable format."""
        self._require_response()
        r = self._last_response
        print(f"[{self.provider} / {self.model}]")
        print(r.content)
        print(
            f"\n(tokens — prompt: {r.prompt_tokens}, "
            f"completion: {r.completion_tokens}, "
            f"total: {self.total_tokens()})"
        )

    # -- Token helper -------------------------------------------------------

    def total_tokens(self) -> int:
        self._require_response()
        return self._last_response.prompt_tokens + self._last_response.completion_tokens

    # -- Internal helpers ---------------------------------------------------

    def _require_response(self) -> None:
        if self._last_response is None:
            raise ResponseError(
                "No response available. Call send_message() first.",
                provider="openrouter",
            )