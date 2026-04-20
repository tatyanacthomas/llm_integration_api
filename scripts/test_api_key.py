# scripts/test_api_key.py
import os
from dotenv import load_dotenv

load_dotenv()

from llm_integration_api.open_router_impl.open_router_client import OpenRouterClient
from llm_integration_api.open_router_impl.open_router_message import OpenRouterMessage


def test_api_key() -> None:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENROUTER_API_KEY not set in .env")

    print(f"API key found: {api_key[:8]}...")

    client = OpenRouterClient(
        api_key=api_key,
        model="openai/gpt-4o-mini",
    )

    history = [
        OpenRouterMessage("user", "Reply with exactly three words: API key works."),
    ]

    print("Contacting OpenRouter...")
    client.send_message(history)
    client.display_response()


if __name__ == "__main__":
    test_api_key()