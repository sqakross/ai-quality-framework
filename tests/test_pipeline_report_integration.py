from reports.quality_report import QualityReport

class FakePipeline:
    def evaluate(self, question, answer, reference_answer):
        if answer == reference_answer:
            return {"status": "PASS", "overall_passed": True}
        return {"status": "FAIL", "overall_passed": False}

def test_pipeline_results_added_to_report():
    report = QualityReport()

    pipeline = FakePipeline()
    result = pipeline.evaluate("Q", "A", "A")

    report.add_result(result)

    assert report.count_pass() == 1

def test_batch_evaluation():
    report = QualityReport()
    pipeline = FakePipeline()

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

    for test_case in test_cases:
        result = pipeline.evaluate(
            test_case["question"],
            test_case["answer"],
            test_case["reference_answer"]
        )

        report.add_result(result)

    assert len(report.results) == 2
    assert report.count_pass() == 1
    assert report.count_fail() == 1
    assert report.pass_rate() == 50