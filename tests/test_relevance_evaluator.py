import json
from evaluators.relevance import RelevanceEvaluator

class FakeJudge:

    def __init__(self, score, reason):
        self.score = score
        self.reason = reason

    def evaluate(self, prompt):
        return json.dumps({
            "score": self.score,
            "reason": self.reason
        })

def test_relevant_answer_passes():
    fake_judge = FakeJudge(5, "Fully relevant")
    evaluator = RelevanceEvaluator(judge_client=fake_judge, threshold=4)

    result = evaluator.evaluate(
        question="test question",
        answer="test answer"
    )

    assert result["passed"] == True

def test_irrelevant_answer_fails():
    fake_judge = FakeJudge(2, "Mostly irrelevant")
    evaluator = RelevanceEvaluator(judge_client=fake_judge, threshold=4)

    result = evaluator.evaluate(
        question="test question",
        answer="test answer"
    )

    assert result["passed"] == False

