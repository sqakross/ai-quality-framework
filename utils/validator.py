def validate_confidence(confidence):
    if not 0 <= confidence <= 1:
        raise ValueError("Confidence must be between 0 and 1")

    return True