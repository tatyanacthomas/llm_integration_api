# LLM Integration API

Minimal provider-agnostic Python interfaces for building LLM integrations.

## Repository Contents

### Root

- `pyproject.toml`
	- Project metadata and tooling configuration.
- `README.md`
	- This guide.

### Package: `llm_integration_api/`

- `client.py`
	- Defines abstract class `Client`.
	- Requires provider/model/api key properties and messaging/response methods.
- `message.py`
	- Defines abstract class `Message` with required `role` and `content` properties.
- `response.py`
	- Defines abstract class `Response` with required `content`, `prompt_tokens`, and
		`completion_tokens` properties.
- `exceptions.py`
	- Defines `LLMIntegrationError` base exception and provider/request/message/response
		specific subclasses.

### Tests: `llm_integration_api/tests/`

- `test_client.py`
	- Verifies `Client` abstract contract and concrete property behavior.
- `test_message.py`
	- Verifies `Message` abstract contract and concrete property behavior.
- `test_response.py`
	- Verifies `Response` abstract contract and concrete property behavior.
- `test_exceptions.py`
	- Verifies exception inheritance and metadata (`provider`, `cause`) behavior.

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

## Setup

From the repository root, create/sync the environment and install development
dependencies:

```bash
uv sync --extra dev
```

If you want to activate the virtual environment manually:

```bash
source .venv/bin/activate
```

## Running Tests

Run the full test suite:

```bash
pytest -q
```