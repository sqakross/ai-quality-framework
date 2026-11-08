import pytest
import json

import evaluators
from evaluators.correctness import CorrectnessEvaluator


@pytest.mark.parametrize("score, expected", [
    (1, False),
    (2, False),
    (4, True),
    (5, True)
])
def test_is_pass(score, expected):
    evaluator = CorrectnessEvaluator(threshold=4)

    actual = evaluator.is_pass(score)

    assert actual == expected


class FakeJudge:

    def __init__(self, score, reason):
        self.score = score
        self.reason = reason

    def evaluate(self, prompt):
        return json.dumps({
            "score": self.score,
            "reason": self.reason
        })


def test_evaluate_passes_for_high_score():
    fake_judge = FakeJudge(4, "Correct")
    evaluators = CorrectnessEvaluator(judge_client=fake_judge,threshold=4)

    result = evaluators.evaluate(
        question="test question",
        answer="test answer",
        reference_answer="test reference"
    )

    assert result["passed"] == True

def test_evaluate_fails_for_low_score():
    fake_judge = FakeJudge(2, "Incorrect")
    evaluators = CorrectnessEvaluator(judge_client=fake_judge,threshold=4)

    result = evaluators.evaluate(
        question="test question",
        answer="test answer",
        reference_answer="test reference"
    )

    assert result["passed"] == False

def test_evaluate_rejects_invalid_score():
    fake_judge = FakeJudge(
        score=8,
        reason="Invalid score"
    )

    evaluators = CorrectnessEvaluator(
        judge_client=fake_judge,
        threshold=4
    )

    with pytest.raises(ValueError):
        evaluators.evaluate(
            question="test question",
            answer="test answer",
            reference_answer="test reference"
        )

class FakeJudgeWithoutScore:
    def evaluate(self, prompt):
        return '{"reason": "Correct"}'

def test_evaluate_rejects_missing_score():
    fake_judge = FakeJudgeWithoutScore()

    evaluators = CorrectnessEvaluator(
        judge_client=fake_judge,
        threshold=4
    )

    with pytest.raises(ValueError):
        evaluators.evaluate(
            question="test question",
            answer="test answer",
            reference_answer="test reference"
        )

class FakeJudgeInvalidJSON:
    def evaluate(self, prompt):
        return "This is not JSON"

def test_evaluate_rejects_invalid_json():
    fake_judge = FakeJudgeInvalidJSON()

    evaluator = CorrectnessEvaluator(
        judge_client=fake_judge,
        threshold=4
    )

    with pytest.raises(json.JSONDecodeError):
        evaluator.evaluate(
            question="test question",
            answer="test answer",
            reference_answer="test reference"
        )
