def validate_future_response(text: str) -> bool:
    required_keywords = [
        "SCENARIO 1",
        "SCENARIO 2",
        "SCENARIO 3"
    ]

    for keyword in required_keywords:
        if keyword not in text:
            return False

    return True
