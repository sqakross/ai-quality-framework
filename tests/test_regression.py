from evaluators.regression import detect_regression, compare_metrics, build_regression_report


def test_regression_detected():
    assert detect_regression(0.95, 0.80) is True


def test_no_regression():
    assert detect_regression(0.80, 0.95) is False


def test_equal_scores():
    assert detect_regression(0.90, 0.90) is False

def test_regression_tolerance():
    assert detect_regression(0.95, 0.94) is False
    assert detect_regression(0.95, 0.90) is True
    assert detect_regression(0.95, 0.95) is False
    assert detect_regression(0.95, 0.98) is False

def test_compare_metrics():
    baseline = {
        "precision": 0.95,
        "recall": 0.90,
        "f1": 0.92
    }

    current = {
        "precision": 0.94,
        "recall": 0.80,
        "f1": 0.86
    }

    result = compare_metrics(baseline, current)

    assert result["precision"] is False
    assert result["recall"] is True
    assert result["f1"] is True

def test_build_regression_report():
    baseline = {
        "precision": 0.95,
        "recall": 0.90,
        "f1": 0.92
    }

    current = {
        "precision": 0.85,
        "recall": 0.90,
        "f1": 0.88
    }

    report = build_regression_report(baseline, current)

    assert report["has_regression"] is True
    assert report["regressions"]["precision"] is True
    assert report["regressions"]["recall"] is False
    assert report["regressions"]["f1"] is True

import json


def test_save_regression_report(tmp_path):
    baseline = {"precision": 0.95, "recall": 0.90, "f1": 0.92}
    current = {"precision": 0.85, "recall": 0.90, "f1": 0.88}

    report = build_regression_report(baseline, current)

    file_path = tmp_path / "regression_report.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    with open(file_path, "r", encoding="utf-8") as file:
        saved_report = json.load(file)

    assert saved_report == report
    assert saved_report["has_regression"] is True