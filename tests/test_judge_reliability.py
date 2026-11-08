from clients.judge_client import JudgeClient
from evaluators.correctness import CorrectnessEvaluator

def test_judge_reliability():
    judge = JudgeClient()
    evaluator = CorrectnessEvaluator(judge_client=judge)

    scores = []
    decisions = []

    for i in range(3):
        result = evaluator.evaluate(
            question="Name the three primary colors of light.",
            answer="Red and green.",
            reference_answer="Red, green, and blue."
        )

        scores.append(result["score"])
        decisions.append(result["passed"])

    print("Judge scores:", scores)

    minimum = min(scores)
    maximum = max(scores)
    score_range = maximum - minimum

    print("Minimum score:", minimum)
    print("Maximum score:", maximum)
    print("Score range:", score_range)
    print("Judge decisions:", decisions)

    assert all(decision is False for decision in decisions)
    assert score_range <= 1