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