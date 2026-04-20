# LLM Integration API

Minimal provider-agnostic Python interfaces for building LLM integrations.

## Repository Contents

### Root

- `pyproject.toml` — project metadata and tooling configuration.
- `uv.lock` — locked dependency versions for reproducible installs.
- `README.md` — this guide.

### Abstract interfaces: `llm_integration_api/interface/`

The provider-agnostic contracts that all implementations must satisfy.

- `client.py` — abstract class `Client` with required `provider`, `api_key`, and `model`
  properties plus `get_message()`, `send_message()`, `get_response()`, and
  `display_response()` methods.
- `message.py` — abstract class `Message` with required `role` and `content` properties.
- `response.py` — abstract class `Response` with required `content`, `prompt_tokens`,
  and `completion_tokens` properties.
- `exceptions.py` — `LLMIntegrationError` base exception and the full hierarchy of
  provider, request, message, and response specific subclasses.

### Interface tests: `llm_integration_api/interface/tests/`

- `test_client.py` — verifies `Client` abstract contract and concrete property behavior.
- `test_message.py` — verifies `Message` abstract contract and concrete property behavior.
- `test_response.py` — verifies `Response` abstract contract and concrete property behavior.
- `test_exceptions.py` — verifies exception inheritance and metadata (`provider`, `cause`) behavior.

### OpenRouter implementation: `llm_integration_api/open_router_impl/`

A ready-to-use implementation targeting the [OpenRouter](https://openrouter.ai) API.
OpenRouter provides a unified endpoint for hundreds of models from providers such as
OpenAI, Anthropic, Google, and others.

- `open_router_client.py` — `OpenRouterClient`, a concrete `Client` that posts conversation
  history to `https://openrouter.ai/api/v1/chat/completions` and returns an
  `OpenRouterResponse`. Constructor args: `api_key`, `model` (any OpenRouter model slug,
  e.g. `"openai/gpt-4o"` or `"anthropic/claude-3.5-sonnet"`), optional `site_url` and
  `app_name` forwarded as `HTTP-Referer` / `X-Title` headers.
- `open_router_message.py` — `OpenRouterMessage`, a concrete `Message` that validates
  `role` (`"system"`, `"user"`, or `"assistant"`) and non-empty `content`.
- `open_router_response.py` — `OpenRouterResponse`, a concrete `Response` that parses the
  raw JSON dict returned by OpenRouter and exposes `content`, `prompt_tokens`, and
  `completion_tokens`.

### OpenRouter tests: `llm_integration_api/open_router_impl/tests/`

- `test_open_router_client.py` — client behavior, error handling, and HTTP edge cases.
- `test_open_router_message.py` — role validation and empty-content guards.
- `test_open_router_response.py` — response parsing and malformed payload handling.

### Scripts: `scripts/`

Runnable scripts for manual testing and exploration. Both scripts read
`OPENROUTER_API_KEY` from a `.env` file in the project root.

- `explore_model.py` — sends several example prompts
  to `openai/gpt-4o-mini` and prints each response. Run with:
  ```bash
  uv run scripts/explore_model.py
  ```
- `test_api_key.py` — quick sanity-check that verifies the API key is set and that
  OpenRouter accepts it. Run with:
  ```bash
  uv run scripts/test_api_key.py
  ```

### Example usage

```python
from llm_integration_api.open_router_impl.open_router_client import OpenRouterClient
from llm_integration_api.open_router_impl.open_router_message import OpenRouterMessage

client = OpenRouterClient(
    api_key="your-openrouter-api-key",
    model="openai/gpt-4o",
    site_url="https://yourapp.example.com",  # optional
    app_name="My App",                        # optional
)

history = [
    OpenRouterMessage("system", "You are a helpful assistant."),
    OpenRouterMessage("user", "What is the capital of France?"),
]

client.send_message(history)
client.display_response()
```

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

## Using This API in Another Project
You can consume this repository directly from GitHub using `uv`. From your other project's root directory:

```bash
uv add "llm-integration-api @ git+https://github.com/tatyanacthomas/llm_integration_api.git"
```

Then install/sync dependencies:

```bash
uv sync
```

You can now import from this package in your project code, for example:

```python
from llm_integration_api.client import Client
from llm_integration_api.message import Message
from llm_integration_api.response import Response
```