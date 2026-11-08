class ClassificationMetrics:
    def __init__(self):
        self.tp = 0
        self.fp = 0
        self.fn = 0
        self.tn = 0

    def update(self, expected_failed, predicted_failed):
        if expected_failed and predicted_failed:
            self.tp += 1

        elif not expected_failed and predicted_failed:
            self.fp += 1

        elif expected_failed and not predicted_failed:
            self.fn += 1

        elif not expected_failed and not predicted_failed:
            self.tn += 1

    def confusion_matrix(self):
        return {
            "TP": self.tp,
            "FP": self.fp,
            "FN": self.fn,
            "TN": self.tn
        }

    def precision(self):
        denominator = self.tp + self.fp

        if denominator == 0:
            return 0.0

        return self.tp / denominator

    def recall(self):
        denominator = self.tp + self.fn

        if denominator == 0:
            return 0.0

        return self.tp / denominator

    def f1_score(self):
        precision = self.precision()
        recall = self.recall()

        if precision + recall == 0:
            return 0.0

        return 2 * precision * recall / (precision + recall)