
import json
from pathlib import Path

import pytest



PROJECT_ROOT = Path(__file__).resolve().parents[2]

with open(PROJECT_ROOT / "test_cases.json", encoding="utf-8") as file:
    test_cases = json.load(file)


@pytest.mark.parametrize(
    "test_case",
    test_cases,
    ids=[case["id"] for case in test_cases],
)
def test_shopassist_policy_response(test_case, shopassist_response):
    question = test_case["input"]
    result = shopassist_response(test_case)
    answer = result["answer"]


    print(f"\nTest Case: {test_case['id']}")
    print(f"Category: {test_case['category']}")
    print(f"Question: {question}")
    print(f"Actual Answer: {answer}")
    print(f"Expected Behavior: {test_case['expected_output']}")

    assert answer.strip(), (
        f"{test_case['id']}: Chatbot returned an empty response."
    )
    if test_case["id"] == "TC_001":
        answer_lower = answer.lower()

        assert "14 days" in answer_lower or "14 calendar days" in answer_lower, (
            "TC_001 FAILED: ShopAssist must state the "
            "14-day return window, not an incorrect duration. "
            f"Actual answer: {answer}"
        )