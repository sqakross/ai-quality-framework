import pytest
from utils.validator import validate_confidence

@pytest.mark.smoke
def test_ai_response(ai_response):
    assert "request_id" in ai_response
    assert isinstance(ai_response["answer"], str)
    assert ai_response["answer"]
    assert 0 <= ai_response["confidence"] <= 1
    assert len(ai_response["sources"]) > 0

@pytest.mark.parametrize("confidence", [
    0,
    0.01,
    0.5,
    0.99,
    1
])

def test_valid_confidence(confidence):
    assert validate_confidence(confidence)

@pytest.mark.parametrize("confidence", [
    -1,
    -0.01,
    1.01,
    10
])
def test_invalid_confidence(confidence):
    with pytest.raises(ValueError):
        validate_confidence(confidence)