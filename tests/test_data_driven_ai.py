from clients.ai_client import AIClient
from config.settings import BASE_URL
from clients.judge_client import JudgeClient
from evaluators.correctness import CorrectnessEvaluator
from evaluators.relevance import RelevanceEvaluator
from evaluators.pipeline import EvaluationPipeline
from reports.quality_report import QualityReport
import json

def test_data_driven_ai(tmp_path):
    test_cases = [
        {
            "question": "What is the capital of France?",
            "reference_answer": "Paris"
        },
        {
            "question": "What is the capital of Germany?",
            "reference_answer": "Berlin"
        },
        {
            "question": "What is 2 + 2?",
            "reference_answer": "4"
        }
    ]

    client = AIClient(BASE_URL)

    judge = JudgeClient()

    report = QualityReport()

    correctness = CorrectnessEvaluator(judge_client=judge)
    relevance = RelevanceEvaluator(judge_client=judge)

    pipeline = EvaluationPipeline(
        correctness_evaluator=correctness,
        relevance_evaluator=relevance
    )

    for test_case in test_cases:
        response = client.send_message(test_case["question"])
        assert response.status_code == 200

        answer = response.json()["answer"]

        result = pipeline.evaluate(
            question=test_case["question"],
            answer=answer,
            reference_answer=test_case["reference_answer"]
        )

        report.add_result(result)

        print(test_case["question"], "->", result["status"])

    assert report.count_fail() == 3
    assert report.count_pass() == 0
    assert report.count_error() == 0
    assert report.pass_rate() == 0

    report_file = tmp_path / "data_driven_report.json"

    report.save_json(report_file)

    assert report_file.exists()
