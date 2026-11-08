

def detect_regression(baseline_f1, current_f1, tolerance=0.02):
    return current_f1 < baseline_f1 - tolerance

def compare_metrics(baseline, current, tolerance=0.02):
    regressions = {}

    for metric in ("precision", "recall", "f1"):
        regressions[metric] = detect_regression(
            baseline[metric],
            current[metric],
            tolerance
        )

    return regressions

def build_regression_report(baseline, current):
    regressions = compare_metrics(baseline, current)

    return {
        "baseline": baseline,
        "current": current,
        "regressions": regressions,
        "has_regression": any(regressions.values())
    }