
import json
from pathlib import Path


def test_cannot_cancel_shipped_order(shopassist_response):
    # Load the existing cancellation test case (TC_003)
    dataset_path = Path(__file__).resolve().parents[2] / "test_cases.json"

    with open(dataset_path, encoding="utf-8") as file:
        test_cases = json.load(file)

    test_case = next(
        case for case in test_cases if case["id"] == "TC_003"
    )

    # Use cached response by default, or live response with --live
    result = shopassist_response(test_case)
    answer = result["answer"]

    print(f"\nShopAssist answer: {answer}")

    answer_lower = answer.lower()

    assert "cannot be cancelled" in answer_lower, (
        "ShopAssist should explain that shipped orders cannot be cancelled."
    )

    assert "return" in answer_lower, (
        "ShopAssist should mention the option of returning an eligible item."
    )
