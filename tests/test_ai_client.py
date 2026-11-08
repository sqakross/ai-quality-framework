
def  test_get_health_returns_ok(ai_client):
    response = ai_client.get_health()
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

