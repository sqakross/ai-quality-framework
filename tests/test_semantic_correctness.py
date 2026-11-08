from clients.judge_client import JudgeClient
from evaluators.correctness import CorrectnessEvaluator


def test_semantic_correctness():
    judge = JudgeClient()
    evaluator = CorrectnessEvaluator(judge_client=judge)

    result = evaluator.evaluate(
        question="What is the capital of France?",
        answer="The capital city of France is Paris.",
        reference_answer="Paris"
    )

    assert result["passed"] is True
    assert result["score"] >= 4

def test_partial_correctness():
    judge = JudgeClient()
    evaluator = CorrectnessEvaluator(judge_client=judge)

    result = evaluator.evaluate(
        question="Name the three primary colors of light.",
        answer="Red and green.",
        reference_answer="Red, green, and blue."
    )

    assert result["passed"] is False
    assert result["score"] < 4

def test_hallucination_detection():
    judge = JudgeClient()
    evaluator = CorrectnessEvaluator(judge_client=judge)

    result = evaluator.evaluate(
        question="Who was the first person to walk on the Moon?",
        answer="Yuri Gagarin was the first person to walk on the Moon in 1961.",
        reference_answer="Neil Armstrong in 1969."
    )

    assert result["passed"] is False
    assert result["score"] <= 2

def test_judge_score_ranking():
    judge = JudgeClient()
    evaluator = CorrectnessEvaluator(judge_client=judge)

    cases = [
        ("The capital of France is Paris.", "Paris"),
        ("Red and green.", "Red, green, and blue."),
        ("Yuri Gagarin walked on the Moon in 1961.", "Neil Armstrong in 1969.")
    ]

    questions = [
        "What is the capital of France?",
        "Name the three primary colors of light.",
        "Who was the first person to walk on the Moon?"
    ]

    scores = []

    for question, (answer, reference) in zip(questions, cases):
        result = evaluator.evaluate(question, answer, reference)
        scores.append(result["score"])

    print("Judge scores:", scores)

    assert scores[0] > scores[1] > scores[2]