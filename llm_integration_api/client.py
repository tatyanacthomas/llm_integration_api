from abc import ABC, abstractmethod

from .exceptions import ClientError, MessageError

class Client(ABC):
    """Abstract base class representing an LLM Client."""
    
    @property
    @abstractmethod
    def provider(self) -> str:
        """Return the provider of the client.

        Concrete implementations should normally return a stored value
        without error. If the client object is in an invalid or unusable state,
        implementations may raise ClientError or a more specific client-related
        subtype.
        
        """
        raise ClientError("Subclasses must implement Client.provider")

    @property
    @abstractmethod
    def api_key(self) -> str:
        """Return the API key of the client.

        Concrete implementations should normally return a stored value
        without error. If the client object is in an invalid or unusable state,
        implementations may raise ClientError or a more specific client-related
        subtype.
        
        """
        raise ClientError("Subclasses must implement Client.api_key")

    @property
    @abstractmethod
    def model(self) -> str:
        """Return the model of the client.

        Concrete implementations should normally return a stored value
        without error. If the client object is in an invalid or unusable state,
        implementations may raise ClientError or a more specific client-related
        subtype.
        
        """
        raise ClientError("Subclasses must implement Client.model")
    
    # Message methods-----------------------------------------------------------------------------------------------------------
    @abstractmethod
    def get_message(self) -> dict:
        # returns {"role": self.role, "content": self.content}
        # most providers expect messages in this dict format
        raise MessageError("Subclasses must implement Client.get_message")

    @abstractmethod
    def send_message(self, history: list) -> "Response":
        # sends the message to the provider and returns an Response object
        raise ClientError("Subclasses must implement Client.send_message")


        
    # Response methods-----------------------------------------------------------------------------------------------------------
    @abstractmethod
    def get_response(self) -> dict:
        # returns all response fields as a dict for easy inspection or logging
        raise ClientError("Subclasses must implement Client.get_response")

    @abstractmethod
    def display_response(self) -> None:
        # prints the response content to the console in a readable format
        raise ClientError("Subclasses must implement Client.display_response")

    def total_tokens(self) -> int:
        # small but useful helper — returns prompt_tokens + completion_tokens
        return self.prompt_tokens + self.completion_tokens