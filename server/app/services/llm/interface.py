from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    content: str
    model: str


class LLMProvider(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:
        """Generate a response from the LLM."""
        raise NotImplementedError
