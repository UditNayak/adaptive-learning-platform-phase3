from app.config import settings
from app.llm.groq_provider import GroqProvider
from app.llm.base_provider import BaseLLMProvider


def get_llm_provider() -> BaseLLMProvider:
    if settings.LLM_PROVIDER.lower() == "groq":
        return GroqProvider()

    raise ValueError("Unsupported LLM provider")