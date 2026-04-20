from abc import ABC, abstractmethod

from .exceptions import MessageError

class Message(ABC):
    """Abstract base class representing a message."""

    @property
    @abstractmethod
    def role(self) -> str:
        """Return the role of the message.

        Concrete implementations should normally return a stored role
        without error. If the message object is in an invalid or unusable state,
        implementations may raise MessageError or a more specific message-related
        subtype.
        """
        raise MessageError("Subclasses must implement Message.role")

    @property
    @abstractmethod
    def content(self) -> str:
        """Return the content of the message.

        Concrete implementations should normally return a stored content
        without error. If the message object is in an invalid or unusable state,
        implementations may raise MessageError or a more specific message-related
        subtype.
        """
        raise MessageError("Subclasses must implement Message.content")
