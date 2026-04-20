import pytest

from llm_integration_api.message import Message


class DummyMessage(Message):
	def __init__(self, role: str, content: str):
		self._role = role
		self._content = content

	@property
	def role(self) -> str:
		return self._role

	@property
	def content(self) -> str:
		return self._content


def test_message_concrete_properties_return_values():
	msg = DummyMessage(role="user", content="Hello")

	assert msg.role == "user"
	assert msg.content == "Hello"


def test_message_cannot_be_instantiated_directly():
	with pytest.raises(TypeError):
		Message()


def test_message_with_missing_abstract_property_is_not_instantiable():
	class IncompleteMessage(Message):
		@property
		def role(self) -> str:
			return "user"

	with pytest.raises(TypeError):
		IncompleteMessage()
