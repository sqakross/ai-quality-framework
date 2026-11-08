from clients.judge_client import JudgeClient
from evaluators.correctness import  CorrectnessEvaluator

def test_correct_answer_passes():
    judge = JudgeClient()

    evaluator = CorrectnessEvaluator(judge_client=judge, threshold=4)

    result = evaluator.evaluate(
        question="What is the capital of France?",
        answer="Paris is the capital of France.",
        reference_answer="Paris"
    )

    assert result["passed"]

