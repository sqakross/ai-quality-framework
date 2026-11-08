from evaluators.regression import build_regression_report
from evaluators.quality_gate import check_quality_gate


def run_quality_pipeline(baseline, current, min_f1=0.85):
    regression_report = build_regression_report(
        baseline,
        current
    )

    decision = check_quality_gate(
        regression_report,
        current_f1=current["f1"],
        min_f1=min_f1
    )

    return {
        "decision": decision,
        "regression_report": regression_report
    }