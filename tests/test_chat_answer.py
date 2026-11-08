def test_chat_returns_answer(ai_client):
    response = ai_client.send_message(
        "What is the capital of France?"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Paris"
    assert "answer" in data
    assert len(data["answer"]) > 0
    assert isinstance(data["answer"], str)
