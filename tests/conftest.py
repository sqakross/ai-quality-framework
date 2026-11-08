import pytest
from clients.ai_client import AIClient
from config.settings import BASE_URL

@pytest.fixture
def ai_response():
    return {
        "request_id": "req-1024",
        "model": "gpt-test",
        "answer": "Your order will arrive tomorrow.",
        "confidence": 0.91,
        "sources": ["order_123.json"]
    }

@pytest.fixture
def ai_client():
    return AIClient(BASE_URL)