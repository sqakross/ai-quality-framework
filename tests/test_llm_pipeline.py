from clients.judge_client import JudgeClient
from evaluators.relevance import RelevanceEvaluator
from evaluators.pipeline import EvaluationPipeline
from evaluators.correctness import CorrectnessEvaluator
from evaluators.batch_runner import BatchRunner
import json

def test_pipeline_with_real_judge():
    judge = JudgeClient()

    relevance = RelevanceEvaluator(judge_client=judge, threshold=4)
    correctness = CorrectnessEvaluator(judge_client=judge, threshold=4)

    pipeline = EvaluationPipeline(correctness_evaluator=correctness, relevance_evaluator=relevance)

    result = pipeline.evaluate(
        question="What is the capital of France?",
        answer="Paris is the capital of France.",
        reference_answer="Paris is the capital of France."
    )

    assert result["overall_passed"]

def test_real_llm_batch_runner(tmp_path):
    judge = JudgeClient()

    correctness = CorrectnessEvaluator( judge_client=judge, threshold=4
    )
    relevance = RelevanceEvaluator(
        judge_client=judge, threshold=4
    )

    pipeline = EvaluationPipeline(
        correctness_evaluator=correctness,
        relevance_evaluator=relevance
    )

    runner = BatchRunner(pipeline)

    test_cases = [
        {
            "question": "Capital of France?",
            "answer": "Paris",
            "reference_answer": "Paris"
        },
        {
            "question": "Capital of Germany?",
            "answer": "Munich",
            "reference_answer": "Berlin"
        }
    ]

    report = runner.run_and_save(test_cases, tmp_path / "real_ai_report.json")

    report_file = tmp_path / "real_ai_report.json"

    assert report_file.exists()

    with open(report_file, encoding="utf-8") as file:
        saved_report = json.load(file)

    assert report.count_pass() == 1
    assert report.count_fail() == 1
    assert report.pass_rate() == 50

    assert saved_report["total"] == 2
    assert saved_report["passed"] == 1
    assert saved_report["failed"] == 1
    assert saved_report["errors"] == 0
    assert saved_report["pass_rate"] == 50
