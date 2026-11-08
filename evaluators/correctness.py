import json

class CorrectnessEvaluator:

    def __init__(self, judge_client=None, threshold=4):
        self.judge_client = judge_client
        self.threshold = threshold

    def is_pass(self, score):
        return score >= self.threshold

    def build_prompt(self, question, answer, reference_answer):
        return f"""
    Evaluate the AI answer for factual correctness.
    
    Treat the REFERENCE ANSWER as the ground truth for this evaluation.
    Do not correct, override, or replace the reference answer using your own knowledge.
    Evaluate whether the AI ANSWER is consistent with the REFERENCE ANSWER.


    QUESTION:
    {question}

    REFERENCE ANSWER:
    {reference_answer}

    AI ANSWER:
    {answer}

    Score:
    1 = Completely incorrect or contradicts the reference answer.
    2 = Contains very little correct information; most required facts are missing or wrong.
    3 = Partially correct; contains some required facts but misses important information.
    4 = Substantially correct; all essential facts are present, with only minor inaccuracies.
    5 = Fully correct; all required facts are accurate and complete, including equivalent wording.

    Scoring rules:
    - Evaluate factual coverage and accuracy, not exact wording.
    - Missing one of three equally important required facts should normally receive score 3.
    - Do not award score 4 or 5 when essential facts are missing.
    - Apply the same scoring criteria consistently across evaluations.
    {{
        "score": 1,
        "reason": "explanation"
    }}
    """

    def evaluate(self, question, answer, reference_answer):
        prompt = self.build_prompt(question, answer, reference_answer)

        result = self.judge_client.evaluate(prompt)

        data = json.loads(result)

        if "score" not in data:
            raise ValueError("Judge response does not contain score")

        score = data["score"]

        if not 1 <= score <= 5:
            raise ValueError("Judge score must be between 1 and 5")

        data["passed"] = self.is_pass(score)

        return data

