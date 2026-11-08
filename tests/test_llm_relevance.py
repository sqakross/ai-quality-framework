from clients.judge_client import JudgeClient
from evaluators.relevance import RelevanceEvaluator

def test_relevant_answer_with_real_judge():
    judge = JudgeClient()

    evaluator = RelevanceEvaluator(judge_client=judge, threshold=4)

    result = evaluator.evaluate(
        question="What is the capital of France?",
        answer="Paris is the capital of France."
    )

    assert result["passed"]
