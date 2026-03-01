import json


def parse_explanation_response(raw_response: str) -> dict:
    try:
        return json.loads(raw_response)
    except Exception:
        raise ValueError("Invalid JSON response from LLM")