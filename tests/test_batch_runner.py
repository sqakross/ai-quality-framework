from evaluators.batch_runner import BatchRunner
from reports.quality_report import QualityReport

class FakePipeline:
    def evaluate(self, question, answer, reference_answer):
        if answer == reference_answer:
            return {"status": "PASS"}
        return {"status": "FAIL"}


def test_batch_runner():
    fake_pipeline = FakePipeline()
    runner = BatchRunner(fake_pipeline)

    report = QualityReport()


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

    results = runner.run(test_cases)
    report = QualityReport()

    for result in results:
        report.add_result(result)

    assert len(results) == 2
    assert results[0]["status"] == "PASS"
    assert results[1]["status"] == "FAIL"
    assert report.count_pass() == 1
    assert report.count_fail() == 1
    assert report.pass_rate() == 50

def test_run_report():
    fake_pipeline = FakePipeline()
    runner = BatchRunner(fake_pipeline)

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

    report = runner.run_report(test_cases)

    assert report.count_pass() == 1
    assert report.count_fail() == 1
    assert report.pass_rate() == 50

def test_run_and_save(tmp_path):
    runner = BatchRunner(FakePipeline())

    test_cases = [
        {
            "question": "Capital of France?",
            "answer": "Paris",
            "reference_answer": "Paris"
        }
    ]

    file_path = tmp_path / "quality_report.json"

    report = runner.run_and_save(test_cases, file_path)

    assert report.count_pass() == 1
    assert file_path.exists()
