
import json
from pathlib import Path

import pytest
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric
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
def test_answer_relevancy(case, shopassist_response):
    result = shopassist_response(case)

    test_case = LLMTestCase(
        input=case["input"],
        actual_output=result["answer"],
    )

    metric = AnswerRelevancyMetric(
        threshold=0.8,
        model=GeminiModel(model="gemini-3.1-flash-lite"),
        include_reason=True,
    )

    assert_test(test_case, [metric])
