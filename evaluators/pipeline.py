import httpx

class EvaluationPipeline:

    def __init__(self, correctness_evaluator,relevance_evaluator):
        self.correctness_evaluator = correctness_evaluator
        self.relevance_evaluator = relevance_evaluator

    def evaluate(self, question, answer, reference_answer):

        try:
            correctness_result = self.correctness_evaluator.evaluate(
                question=question,
                answer=answer,
                reference_answer=reference_answer
            )

            relevance_result = self.relevance_evaluator.evaluate(
                question=question,
                answer=answer
            )

            if "passed" not in correctness_result:
                raise ValueError("Correctness result missing passed")

            if "passed" not in relevance_result:
                raise ValueError("Relevance result missing passed")

            if not isinstance(correctness_result["passed"], bool):
                raise ValueError("Correctness passed must be boolean")

            if not isinstance(relevance_result["passed"], bool):
                raise ValueError("Relevance passed must be boolean")

        except (ValueError, httpx.RequestError) as error:

            return {
                "status": "ERROR",
                "correctness": None,
                "relevance": None,
                "overall_passed": None,
                "error": str(error)
            }


        overall_passed = (
            correctness_result["passed"]
            and relevance_result["passed"]
        )


        if overall_passed:
            status = "PASS"
        else:
            status = "FAIL"

        return {
            "status": status,
            "correctness": correctness_result,
            "relevance": relevance_result,
            "overall_passed": overall_passed
        }





