
import json
from pathlib import Path

import pytest
from dotenv import load_dotenv
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.models import GeminiModel
from deepeval.test_case import LLMTestCase, SingleTurnParams



load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

with open(PROJECT_ROOT / "test_cases.json", encoding="utf-8") as file:
    test_cases = json.load(file)


@pytest.mark.parametrize(
    "test_case_data",
    test_cases,
    ids=[case["id"] for case in test_cases],
)
def test_policy_correctness(test_case_data, shopassist_response):
    result = shopassist_response(test_case_data)
    actual_answer = result["answer"]

    print(f"\nTest Case: {test_case_data['id']}")
    print(f"Actual Answer:\n{actual_answer}")

    evaluation_case = LLMTestCase(
        input=test_case_data["input"],
        actual_output=actual_answer,
        expected_output=test_case_data["expected_output"],
    )

    correctness_metric = GEval(
        name="Policy Correctness",
        criteria=(
            "Evaluate whether the actual response accurately follows "
            "the expected ShopAssist policy. Check factual correctness, "
            "eligibility conditions, restrictions, and whether the "
            "response invents unsupported policy information. "
            "Allow different wording when the meaning is correct."
        ),
        evaluation_params=[
            SingleTurnParams.INPUT,
            SingleTurnParams.ACTUAL_OUTPUT,
            SingleTurnParams.EXPECTED_OUTPUT,
        ],
        model=GeminiModel(model="gemini-3.1-flash-lite"),
        threshold=0.8,
    )

    assert_test(evaluation_case, [correctness_metric])
