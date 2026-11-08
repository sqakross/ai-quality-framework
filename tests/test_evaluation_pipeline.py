from evaluators.pipeline import EvaluationPipeline
import pytest
import httpx

class FakeCorrectnessEvaluator:

    def __init__(self, passed):
        self.passed = passed


    def evaluate(self, question, answer, reference_answer):
        return {
            "score": 5,
            "reason": "Correct",
            "passed": self.passed
        }

class FakeRelevanceEvaluator:
    def __init__(self, passed):
        self.passed = passed

    def evaluate(self, question, answer):
        return {
            "score": 2,
            "reason": "Mostly irrelevant",
            "passed": self.passed
        }

class FakeCorrectnessError:

    def evaluate(self, question, answer, reference_answer):
        raise ValueError("Judge score must be between 1 and 5")

class FakeRelevanceError:

    def evaluate(self, question, answer):
        raise ValueError("Relevance evaluation failed")

class FakeCorrectnessMissingPassed:

    def evaluate(self, question, answer, reference_answer):
        return {
            "score": 5,
            "reason": "Correct"
        }

class FakeRelevanceMissingPassed:

    def evaluate(self, question, answer):
        return {
            "score": 5,
            "reason": "Relevant"
        }

class FakeRelevanceInvalidPassed:

    def evaluate(self, question, answer):
        return {
            "score": 2,
            "reason": "Irrelevant",
            "passed": "False"
        }

class FakeCorrectnessNetworkError:

    def evaluate(self, question, answer, reference_answer):
        raise httpx.ConnectError("Cannot connect to Judge API")

@pytest.mark.parametrize(
    "correctness_passed, relevance_passed, expected",
    [
        (True, True, True),
        (True, False, False),
        (False, True, False),
        (False, False, False),
    ]
)
def test_pipeline_fails_when_relevance_fails(correctness_passed, relevance_passed, expected):
    fake_correctness= FakeCorrectnessEvaluator(correctness_passed)
    fake_relevance = FakeRelevanceEvaluator(relevance_passed)

    pipeline = EvaluationPipeline(
        correctness_evaluator=fake_correctness,
        relevance_evaluator=fake_relevance
    )

    result = pipeline.evaluate(
        question="test question",
        answer="test answer",
        reference_answer="test reference answer"
    )

    assert result["overall_passed"] == expected

    if expected:
        assert result["status"] == "PASS"
    else:
        assert result["status"] == "FAIL"


def test_pipeline_raises_error():
    fake_correctness = FakeCorrectnessError()
    fake_relevance = FakeRelevanceEvaluator(True)

    pipeline = EvaluationPipeline(
        correctness_evaluator=fake_correctness,
        relevance_evaluator=fake_relevance
    )

    result = pipeline.evaluate(
        question="What is the capital of France?",
        answer="Paris",
        reference_answer="Paris"
    )

    assert result["status"] == "ERROR"
    assert result["overall_passed"] is None

def test_pipeline_relevance_error():
    fake_correctness = FakeCorrectnessEvaluator(True)
    fake_relevance = FakeRelevanceError()

    pipeline = EvaluationPipeline(
        correctness_evaluator=fake_correctness,
        relevance_evaluator=fake_relevance
    )

    result = pipeline.evaluate(
        question="What is the capital of France?",
        answer="Paris",
        reference_answer="Paris"
    )

    assert result["status"] == "ERROR"
    assert result["overall_passed"] is None
    assert result["error"] == "Relevance evaluation failed"

def test_pipeline_missing_correctness_passed():
    fake_correctness = FakeCorrectnessMissingPassed()
    fake_relevance = FakeRelevanceEvaluator(True)

    pipeline = EvaluationPipeline(
        correctness_evaluator=fake_correctness,
        relevance_evaluator=fake_relevance
    )

    result = pipeline.evaluate(
        question="What is the capital of France?",
        answer="Paris",
        reference_answer="Paris"
    )

    assert result["status"] == "ERROR"
    assert result["overall_passed"] is None
    assert result["error"] == "Correctness result missing passed"

def test_pipeline_missing_relevance_passed():
    fake_correctness = FakeCorrectnessEvaluator(True)
    fake_relevance = FakeRelevanceMissingPassed()

    pipeline = EvaluationPipeline(
        correctness_evaluator=fake_correctness,
        relevance_evaluator=fake_relevance
    )

    result = pipeline.evaluate(
        question="What is the capital of France?",
        answer="Paris",
        reference_answer="Paris"
    )

    assert result["status"] == "ERROR"
    assert result["overall_passed"] is None
    assert result["error"] == "Relevance result missing passed"

def test_pipeline_relevance_invalid_passed():
    fake_correctness = FakeCorrectnessEvaluator(True)
    fake_relevance = FakeRelevanceInvalidPassed()

    pipeline = EvaluationPipeline(
        correctness_evaluator=fake_correctness,
        relevance_evaluator=fake_relevance
    )

    result = pipeline.evaluate(
        question="What is the capital of France?",
        answer="Paris",
        reference_answer="Paris"
    )

    assert result["status"] == "ERROR"
    assert result["overall_passed"] is None
    assert result["error"] == "Relevance passed must be boolean"

def test_pipeline_network_error():
    fake_correctness = FakeCorrectnessNetworkError()
    fake_relevance = FakeRelevanceEvaluator(True)

    pipeline = EvaluationPipeline(
        correctness_evaluator=fake_correctness,
        relevance_evaluator=fake_relevance
    )

    result = pipeline.evaluate(
        question="What is the capital of France?",
        answer="Paris",
        reference_answer="Paris"
    )

    assert result["status"] == "ERROR"
    assert result["overall_passed"] is None
    assert result["error"] in "Cannot connect to Judge API"







