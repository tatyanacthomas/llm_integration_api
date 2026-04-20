from abc import ABC, abstractmethod

from .exceptions import ResponseError

class Response(ABC):
    """Abstract base class representing a response from the provider.""" 

    @property
    @abstractmethod
    def content(self) -> str:
        """Return the content of the response.

        Concrete implementations should normally return a stored content
        without error. If the response object is in an invalid or unusable state,
        implementations may raise ResponseError or a more specific response-related
        subtype.
        """
        raise ResponseError("Subclasses must implement Response.content")

    @property
    @abstractmethod
    def prompt_tokens(self) -> int:
        """Return the number of prompt tokens used in the response.

        Concrete implementations should normally return a stored value
        without error. If the response object is in an invalid or unusable state,
        implementations may raise ResponseError or a more specific response-related
        subtype.
        """
        raise ResponseError("Subclasses must implement Response.prompt_tokens")

    @property
    @abstractmethod
    def completion_tokens(self) -> int:
        """Return the number of completion tokens used in the response.

        Concrete implementations should normally return a stored value
        without error. If the response object is in an invalid or unusable state,
        implementations may raise ResponseError or a more specific response-related
        subtype.
        """
        raise ResponseError("Subclasses must implement Response.completion_tokens")