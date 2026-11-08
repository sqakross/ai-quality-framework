from openai import OpenAI


class JudgeClient:

    def __init__(self):
        self.client = OpenAI()

    def evaluate(self, prompt):
        response = self.client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return response.output_text