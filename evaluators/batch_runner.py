from reports.quality_report import QualityReport

class BatchRunner:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def run(self, test_cases):
        results = []
        for test_case in test_cases:
            result = self.pipeline.evaluate(
                test_case["question"],
                test_case["answer"],
                test_case["reference_answer"]
            )

            results.append(result)

        return results

    def run_report(self, test_cases):
        results = self.run(test_cases)
        report = QualityReport()

        for result in results:
            report.add_result(result)

        return report

    def run_and_save(self, test_cases, file_path):
        report = self.run_report(test_cases)
        report.save_json(file_path)
        return report