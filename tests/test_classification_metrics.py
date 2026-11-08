from evaluators.classification_metrics import ClassificationMetrics
import pytest

def test_classification_metrics():
    metrics = ClassificationMetrics()

    metrics.update(True, True)
    metrics.update(False, True)
    metrics.update(True, False)
    metrics.update(False, False)

    assert metrics.tp == 1
    assert metrics.fp == 1
    assert metrics.fn == 1
    assert metrics.tn == 1
    assert metrics.confusion_matrix() == {
        "TP": 1,
        "FP": 1,
        "FN": 1,
        "TN": 1
    }

    assert metrics.precision() == 0.5
    assert metrics.recall() == 0.5
    assert metrics.f1_score() == 0.5

def test_metrics_with_no_results():
    metrics = ClassificationMetrics()

    assert metrics.tp == 0
    assert metrics.fp == 0
    assert metrics.fn == 0
    assert metrics.tn == 0

    assert metrics.precision() == 0.0
    assert metrics.recall() == 0.0
    assert metrics.f1_score() == 0.0

@pytest.mark.parametrize(
    "expected_failed, predicted_failed, expected_type",
    [
        (True, True, "TP"),
        (False, True, "FP"),
        (True, False, "FN"),
        (False, False, "TN"),
    ]
)
def test_classification_cases(expected_failed, predicted_failed, expected_type):
    metrics = ClassificationMetrics()

    metrics.update(expected_failed, predicted_failed)

    result = metrics.confusion_matrix()

    assert result[expected_type] == 1
    assert sum(result.values()) == 1