
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("DIFY_API_BASE_URL", "https://api.dify.ai/v1")
API_KEY = os.getenv("DIFY_API_KEY")


def ask_shopassist_with_context(question: str) -> dict:
    """Return the chatbot answer and retrieved knowledge chunks."""

    if not API_KEY:
        raise ValueError("DIFY_API_KEY is missing from .env")

    response = requests.post(
        f"{BASE_URL.rstrip('/')}/chat-messages",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "inputs": {},
            "query": question,
            "response_mode": "blocking",
            "conversation_id": "",
            "user": "shopassist-qa-test",
        },
        timeout=120,
    )

    if not response.ok:
        raise RuntimeError(
            f"Dify API error ({response.status_code}): {response.text}"
        )

    data = response.json()

    resources = (data.get("metadata") or {}).get(
        "retriever_resources"
    ) or []

    retrieval_context = [
        resource["content"]
        for resource in resources
        if resource.get("content")
    ]

    return {
        "answer": data["answer"],
        "retrieval_context": retrieval_context,
    }


def ask_shopassist(question: str) -> str:
    """Return only the chatbot answer for existing tests."""
    return ask_shopassist_with_context(question)["answer"]
