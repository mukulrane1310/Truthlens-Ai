from groq import Groq

from app.core.config import settings
from app.services.llm.interface import LLMProvider, LLMResponse


class GroqProvider(LLMProvider):

    def __init__(self, model: str | None = None) -> None:
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = model or settings.GROQ_MODEL

    def generate(self, prompt: str) -> LLMResponse:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        content = response.choices[0].message.content or ""

        return LLMResponse(
            content=content,
            model=self.model,
        )
