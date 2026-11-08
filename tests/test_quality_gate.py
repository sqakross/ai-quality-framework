from evaluators.quality_gate import check_quality_gate


def test_quality_gate_blocks_regression():
    report = {"has_regression": True}

    result = check_quality_gate(report, current_f1=0.90)

    assert result == "BLOCKED"


def test_quality_gate_approves_release():
    report = {"has_regression": False}

    result = check_quality_gate(report, current_f1=0.90)

    assert result == "APPROVED"

def test_quality_gate_blocks_low_f1():
    report = {"has_regression": False}

    result = check_quality_gate(report, current_f1=0.70)

    assert result == "BLOCKED"

def test_quality_gate_at_threshold():
    report = {"has_regression": False}

    result = check_quality_gate(report, current_f1=0.85)

    assert result == "APPROVED"


def test_quality_gate_below_threshold():
    report = {"has_regression": False}

    result = check_quality_gate(report, current_f1=0.84)

    assert result == "BLOCKED"

def test_quality_gate_custom_threshold():
    report = {"has_regression": False}

    result = check_quality_gate(
        report,
        current_f1=0.90,
        min_f1=0.95
    )

    assert result == "BLOCKED"