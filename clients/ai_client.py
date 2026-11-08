import httpx

class AIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_health(self):
        return httpx.get(f"{self.base_url}/health")

    def send_message(self, question):
        return httpx.post(f"{self.base_url}/chat", json={"question": question})

