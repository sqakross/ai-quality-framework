from clients.judge_client import JudgeClient
from evaluators.correctness import CorrectnessEvaluator
from evaluators.classification_metrics import ClassificationMetrics
import json

def test_judge_benchmark(tmp_path):
    test_cases = [
        {
            "question": "What is the capital of France?",
            "answer": "Paris",
            "reference_answer": "Paris",
            "expected_failed": False
        },
        {
            "question": "What is the capital of France?",
            "answer": "London",
            "reference_answer": "Paris",
            "expected_failed": True
        },
        {
            "question": "What is the capital of Germany?",
            "answer": "Berlin",
            "reference_answer": "Berlin",
            "expected_failed": False
        },
        {
            "question": "What is the capital of Germany?",
            "answer": "Munich",
            "reference_answer": "Berlin",
            "expected_failed": True
        }
    ]

    errors = []
    case_results = []

    judge = JudgeClient()
    evaluator = CorrectnessEvaluator(judge_client=judge)
    metrics = ClassificationMetrics()

    for test_case in test_cases:
        result = evaluator.evaluate(
            question=test_case["question"],
            answer=test_case["answer"],
            reference_answer=test_case["reference_answer"]
        )

        print(test_case["answer"], "->", result["score"], result["passed"])
        metrics.update(
            expected_failed=test_case["expected_failed"],
            predicted_failed=not result["passed"]
        )
        predicted_failed = not result["passed"]

        case_results.append({
            "question": test_case["question"],
            "answer": test_case["answer"],
            "expected_failed": test_case["expected_failed"],
            "predicted_failed": predicted_failed,
            "score": result["score"],
            "reason": result.get("reason", "")
        })

        if predicted_failed != test_case["expected_failed"]:
            if predicted_failed:
                error_type = "FP"
            else:
                error_type = "FN"
            errors.append({
                "question": test_case["question"],
                "answer": test_case["answer"],
                "expected_failed": test_case["expected_failed"],
                "predicted_failed": predicted_failed,
                "score": result["score"],
                "type": error_type,
                "reason": result.get("reason", "")
            })

        print("Classification errors:", errors)
        print("TP:", metrics.tp)
        print("FP:", metrics.fp)
        print("FN:", metrics.fn)
        print("TN:", metrics.tn)
        print("Precision:", metrics.precision())
        print("Recall:", metrics.recall())
        print("F1-score:", metrics.f1_score())

    assert len(case_results) == len(test_cases)
    print("Detailed case results:", case_results)

    assert len(test_cases) == 4
    assert metrics.tp == 2
    assert metrics.fp == 0
    assert metrics.fn == 0
    assert metrics.tn == 2

    assert metrics.precision() == 1.0
    assert metrics.recall() == 1.0
    assert metrics.f1_score() == 1.0

    report_file = tmp_path / "judge_errors.json"

    with open(report_file, "w", encoding="utf-8") as file:
        json.dump(errors, file, indent=4)

    assert report_file.exists()

    with open(report_file, "r", encoding="utf-8") as file:
        saved_errors = json.load(file)

    assert saved_errors == errors

    quality_summary = {
        "total_cases": len(test_cases),
        "tp": metrics.tp,
        "fp": metrics.fp,
        "fn": metrics.fn,
        "tn": metrics.tn,
        "precision": metrics.precision(),
        "recall": metrics.recall(),
        "f1_score": metrics.f1_score(),
        "errors": errors
    }

    report_data = {
        "total": len(test_cases),
        "tp": metrics.tp,
        "fp": metrics.fp,
        "fn": metrics.fn,
        "tn": metrics.tn,
        "cases": case_results
    }

    report_file = tmp_path / "judge_benchmark_report.json"

    with open(report_file, "w", encoding="utf-8") as file:
        json.dump(report_data, file, indent=4)

    assert quality_summary["total_cases"] == 4
    assert quality_summary["f1_score"] == 1.0
    assert quality_summary["errors"] == []

    assert (
                   quality_summary["tp"]
                   + quality_summary["fp"]
                   + quality_summary["fn"]
                   + quality_summary["tn"]
           ) == quality_summary["total_cases"]

    assert 0.0 <= quality_summary["precision"] <= 1.0
    assert 0.0 <= quality_summary["recall"] <= 1.0
    assert 0.0 <= quality_summary["f1_score"] <= 1.0

    assert report_file.exists()
    assert json.loads(report_file.read_text(encoding="utf-8")) == report_data

def test_error_types():
    cases = [
        {"expected_failed": False, "predicted_failed": True},
        {"expected_failed": True, "predicted_failed": False}
    ]

    errors = []

    for case in cases:
        if case["predicted_failed"] != case["expected_failed"]:
            if case["predicted_failed"]:
                error_type = "FP"
            else:
                error_type = "FN"

            errors.append(error_type)

    assert errors == ["FP", "FN"]

def test_error_report_with_data(tmp_path):
    errors = [
        {
            "question": "What is the capital of France?",
            "answer": "Paris",
            "expected_failed": False,
            "predicted_failed": True,
            "score": 2,
            "type": "FP",
            "reason": "Incorrectly rejected a correct answer"
        }
    ]

    report_file = tmp_path / "judge_errors.json"

    with open(report_file, "w", encoding="utf-8") as file:
        json.dump(errors, file, indent=4)

    with open(report_file, "r", encoding="utf-8") as file:
        saved_errors = json.load(file)

    assert saved_errors == errors
    assert saved_errors[0]["type"] == "FP"
    assert saved_errors[0]["score"] == 2