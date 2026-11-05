
import json
from pathlib import Path

import pytest
from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric
from deepeval.models import GeminiModel
from deepeval.test_case import LLMTestCase


PROJECT_ROOT = Path(__file__).resolve().parents[2]

with open(PROJECT_ROOT / "test_cases.json", encoding="utf-8") as file:
    TEST_CASES = json.load(file)


@pytest.mark.parametrize(
    "case",
    TEST_CASES,
    ids=[case["id"] for case in TEST_CASES],
)
def test_policy_faithfulness(case, shopassist_response):
    result = shopassist_response(case)

    assert result["retrieval_context"], (
        f"No knowledge retrieved for {case['id']}!"
    )

    test_case = LLMTestCase(
        input=case["input"],
        actual_output=result["answer"],
        retrieval_context=result["retrieval_context"],
    )

    metric = FaithfulnessMetric(
        threshold=0.8,
        model=GeminiModel(model="gemini-3.1-flash-lite"),
        include_reason=True,
    )

    assert_test(test_case, [metric])
