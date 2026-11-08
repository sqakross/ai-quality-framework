def check_quality_gate(regression_report, current_f1, min_f1=0.85):
    if regression_report["has_regression"]:
        return "BLOCKED"

    if current_f1 < min_f1:
        return "BLOCKED"

    return "APPROVED"