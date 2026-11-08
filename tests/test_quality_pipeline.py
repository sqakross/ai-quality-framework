from evaluators.quality_pipeline import run_quality_pipeline


def test_quality_pipeline_approved():
    baseline = {
        "precision": 0.90,
        "recall": 0.90,
        "f1": 0.90
    }

    current = {
        "precision": 0.92,
        "recall": 0.91,
        "f1": 0.91
    }

    result = run_quality_pipeline(baseline, current)

    assert result["decision"] == "APPROVED"
    assert result["regression_report"]["has_regression"] is False

def test_quality_pipeline_blocked_by_regression():
    baseline = {
        "precision": 0.95,
        "recall": 0.95,
        "f1": 0.95
    }

    current = {
        "precision": 0.90,
        "recall": 0.90,
        "f1": 0.90
    }

    result = run_quality_pipeline(baseline, current)

    assert result["decision"] == "BLOCKED"
    assert result["regression_report"]["has_regression"] is True

def test_quality_pipeline_blocked_by_low_f1():
    baseline = {"precision": 0.75, "recall": 0.75, "f1": 0.75}
    current = {"precision": 0.80, "recall": 0.80, "f1": 0.80}

    result = run_quality_pipeline(baseline, current)

    assert result["regression_report"]["has_regression"] is False
    assert result["decision"] == "BLOCKED"