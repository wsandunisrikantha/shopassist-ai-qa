
import json
from pathlib import Path

import pytest

from dify_client import ask_shopassist_with_context


PROJECT_ROOT = Path(__file__).resolve().parent
CACHE_DIR = PROJECT_ROOT / "test_data"


def pytest_addoption(parser):
    parser.addoption(
        "--live",
        action="store_true",
        default=False,
        help="Fetch fresh responses from Dify instead of using cached responses.",
    )


@pytest.fixture
def live_mode(request):
    return request.config.getoption("--live")


@pytest.fixture(scope="session")
def response_store():
    return {}


@pytest.fixture
def shopassist_response(request, live_mode, response_store):
    def get_response(case):
        case_id = case["id"]
        question = case["input"]
        cache_path = CACHE_DIR / f"{case_id}_faithfulness.json"

        if case_id in response_store:
            return response_store[case_id]

        if cache_path.exists() and not live_mode:
            print(f"\nLoading cached response for {case_id}...")

            with open(cache_path, encoding="utf-8") as file:
                saved = json.load(file)

            assert saved["input"] == question, (
                f"Cached question mismatch for {case_id}"
            )

            result = {
                "answer": saved["actual_output"],
                "retrieval_context": saved["retrieval_context"],
            }
        else:
            print(f"\nFetching live response for {case_id}...")

            result = ask_shopassist_with_context(question)

            assert result["retrieval_context"], (
                f"No knowledge retrieved for {case_id}!"
            )

            CACHE_DIR.mkdir(parents=True, exist_ok=True)

            with open(cache_path, "w", encoding="utf-8") as file:
                json.dump(
                    {
                        "input": question,
                        "actual_output": result["answer"],
                        "retrieval_context": result["retrieval_context"],
                    },
                    file,
                    indent=2,
                    ensure_ascii=False,
                )

        response_store[case_id] = result
        return result

    return get_response
