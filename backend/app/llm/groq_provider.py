from groq import Groq
from app.config import settings
from app.llm.base_provider import BaseLLMProvider


class GroqProvider(BaseLLMProvider):

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    def generate(self, messages: list[dict]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        return response.choices[0].message.content