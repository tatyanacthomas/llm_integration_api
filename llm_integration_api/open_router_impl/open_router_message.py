from llm_integration_api.interface.message import Message
from llm_integration_api.interface.exceptions import MessageValidationError


class OpenRouterMessage(Message):
    """Concrete Message implementation for OpenRouter."""

    VALID_ROLES = {"system", "user", "assistant"}

    def __init__(self, role: str, content: str) -> None:
        if role not in self.VALID_ROLES:
            raise MessageValidationError(
                f"Invalid role '{role}'. Must be one of {self.VALID_ROLES}.",
                provider="openrouter",
            )
        if not content or not content.strip():
            raise MessageValidationError(
                "Message content must not be empty.",
                provider="openrouter",
            )
        self._role = role
        self._content = content

    @property
    def role(self) -> str:
        return self._role

    @property
    def content(self) -> str:
        return self._content