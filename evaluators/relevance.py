import json

class RelevanceEvaluator:

    def __init__(self, judge_client=None, threshold=4):
        self.judge_client = judge_client
        self.threshold = threshold

    def is_pass(self, score):
        return score >= self.threshold

    def build_prompt(self, question, answer):
        return f"""
    Evaluate how relevant the AI answer is to the user's question.
    
    QUESTION:
    {question}
   
    AI ANSWER:
    {answer}

    Score:
    1 = completely irrelevant
    2 = mostly irrelevant
    3 = partially relevant
    4 = mostly relevant
    5 = fully relevant

    Return ONLY JSON:
    {{
        "score": 1,
        "reason": "explanation"
    }}
    """

    def evaluate(self, question, answer):
        prompt = self.build_prompt(question, answer)

        result = self.judge_client.evaluate(prompt)

        data = json.loads(result)

        if "score" not in data:
            raise ValueError("Judge response does not contain score")

        score = data["score"]

        if not 1 <= score <= 5:
            raise ValueError("Judge score must be between 1 and 5")

        data["passed"] = self.is_pass(score)

        return data