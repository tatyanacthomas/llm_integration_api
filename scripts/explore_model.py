# scripts/explore_model.py
import os
from dotenv import load_dotenv
from pathlib import Path
import time

load_dotenv()

from llm_integration_api.open_router_impl.open_router_client import OpenRouterClient
from llm_integration_api.open_router_impl.open_router_message import OpenRouterMessage

MODEL = "openai/gpt-4o-mini"
DELAY = 30 

def run(system: str, user: str) -> None:
    client = OpenRouterClient(api_key=os.getenv("OPENROUTER_API_KEY"), model=MODEL)
    history = []
    if system:
        history.append(OpenRouterMessage("system", system))
    history.append(OpenRouterMessage("user", user))
    client.send_message(history)
    client.display_response()
    print("-" * 60)
    # time.sleep(DELAY)


if __name__ == "__main__":
    run(
        system="You are a helpful assistant.",
        user="What is the capital of Japan?",
    )
    run(
        system="You are a pirate. Respond only in pirate speak.",
        user="What is the capital of Japan?",
    )
    run(
        system="You are a helpful assistant.",
        user="Give me three one-sentence ideas for a mobile app.",
    )
    run(
        system="",
        user="Explain what an API is in one sentence.",
    )