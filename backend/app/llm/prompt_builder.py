def build_explanation_prompt(topic_name: str, knowledge_level: str, description: str | None):

    return f"""
You are an expert tutor.

Generate a structured JSON response.

Topic: {topic_name}
Level: {knowledge_level}
Additional description: {description or "None"}

Return STRICTLY in JSON format like:

{{
  "title": "Short 4-6 word chat title",
  "explanation": "Detailed explanation here..."
}}

Do not include markdown.
Do not include extra text.
Return valid JSON only.
"""


def build_quiz_prompt(topic_name: str, level: str):

    return f"""
You are an expert tutor.

Generate a quiz(only one question) in STRICT JSON format:

{{
  "question": "Question text",
  "options": {{
      "A": "Option text",
      "B": "Option text",
      "C": "Option text",
      "D": "Option text"
  }},
  "correct_option": "A",
  "points": 10, 
  "hint": "Short hint",
  "explanation": "Detailed explanation"
}}

Topic: {topic_name}
Level: {level}

Points should be based on the level of the question.
Return ONLY valid JSON.
"""