import json


class QualityReport:

    def __init__(self):
        self.results = []

    def add_result(self, result):
        self.results.append(result)

    def total(self):
        return len(self.results)

    def count_pass(self):
        count = 0

        for result in self.results:
            if result["status"] == "PASS":
                count += 1

        return count

    def count_fail(self):
        count = 0

        for result in self.results:
            if result["status"] == "FAIL":
                count += 1

        return count

    def count_error(self):
        count = 0

        for result in self.results:
            if result["status"] == "ERROR":
                count += 1

        return count

    def pass_rate(self):
        passed = self.count_pass()
        failed = self.count_fail()

        total_evaluated = passed + failed

        if total_evaluated > 0:
            return (passed / total_evaluated) * 100

        else:
            return None

    def to_dict(self):
        return {
            "total": len(self.results),
            "passed": self.count_pass(),
            "failed": self.count_fail(),
            "errors": self.count_error(),
            "pass_rate": self.pass_rate()
        }

    def save_json(self, file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(self.to_dict(), file, indent=4)
