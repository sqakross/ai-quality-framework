from clients.ai_client import AIClient
from config.settings import BASE_URL
from clients.judge_client import JudgeClient
from evaluators.correctness import CorrectnessEvaluator
from evaluators.relevance import RelevanceEvaluator
from evaluators.pipeline import EvaluationPipeline
from reports.quality_report import QualityReport

def test_ai_end_to_end():
    client = AIClient(BASE_URL)
    response = client.send_message("What is the capital of France?")

    data = response.json()
    answer = data["answer"]

    judge = JudgeClient()

    correctness = CorrectnessEvaluator(judge_client=judge)
    relevance = RelevanceEvaluator(judge_client=judge)

    pipeline = EvaluationPipeline(
        correctness_evaluator=correctness,
        relevance_evaluator=relevance
    )

    result = pipeline.evaluate(
        question="What is the capital of France?",
        answer=answer,
        reference_answer="Paris"
    )

    report = QualityReport()
    report.add_result(result)

    assert response.status_code == 200
    assert result["status"] == "FAIL"
    assert report.count_fail() == 1
    assert report.count_pass() == 0
    assert report.pass_rate() == 0