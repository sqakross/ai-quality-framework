from reports.quality_report import QualityReport
import json

def test_count_pass():
    report = QualityReport()

    report.add_result({"status": "PASS"})
    assert report.count_pass() == 1

def test_count_fail():
    report = QualityReport()

    report.add_result({"status": "FAIL"})
    assert report.count_fail() == 1

def test_count_error():
    report = QualityReport()

    report.add_result({"status": "ERROR"})
    assert report.count_error() == 1

def test_pass_rate():
    report = QualityReport()

    report.add_result({"status": "PASS"})
    report.add_result({"status": "FAIL"})

    assert report.pass_rate() == 50

def test_pass_rate_only_errors():
    report = QualityReport()
    report.add_result({"status": "ERROR"})

    assert report.pass_rate() is None

def test_to_dict():
    report = QualityReport()

    report.add_result({"status": "PASS"})
    report.add_result({"status": "FAIL"})

    summary = report.to_dict()

    assert summary == {
        "total": 2,
        "passed": 1,
        "failed": 1,
        "errors": 0,
        "pass_rate": 50.0
    }

def test_save_json(tmp_path):
    report = QualityReport()
    report.add_result({"status": "PASS"})
    report.add_result({"status": "FAIL"})

    file_path = tmp_path / "quality_report.json"

    report.save_json(file_path)

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["total"] == 2
    assert data["passed"] == 1
    assert data["failed"] == 1
    assert data["pass_rate"] == 50