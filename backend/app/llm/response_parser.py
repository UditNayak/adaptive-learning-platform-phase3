import json
import re


def extract_json_from_text(text: str) -> str:
    """
    Extract JSON object from LLM response.
    Handles markdown code blocks.
    """

    # Remove markdown code fences
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    # Try to extract first JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)

    return text


def parse_explanation_response(raw_response: str) -> dict:
    try:
        cleaned = extract_json_from_text(raw_response)
        parsed = json.loads(cleaned)

        parsed.setdefault("references", [])

        return parsed

    except Exception:
        print("RAW LLM RESPONSE:")
        print(raw_response)
        raise ValueError("Invalid JSON response from LLM")


def parse_quiz_response(raw_response: str) -> dict:
    try:
        return json.loads(raw_response)
    except Exception:
        raise ValueError("Invalid JSON from LLM")