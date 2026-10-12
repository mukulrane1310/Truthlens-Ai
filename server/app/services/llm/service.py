from app.services.llm.interface import LLMProvider
from app.services.llm.parser import LLMOutputParser
from app.services.llm.prompt import TruthLensPromptBuilder
from app.services.llm.schemas import VerdictResponse
from app.services.rag.interface import RetrievedEvidence


class LLMAnalysisService:

    def __init__(self, provider: LLMProvider) -> None:
        self.provider = provider
        self.prompt_builder = TruthLensPromptBuilder()
        self.parser = LLMOutputParser()

    def analyze(
        self,
        claim: str,
        evidence: list[RetrievedEvidence],
    ) -> VerdictResponse:
        prompt = self.prompt_builder.build(
            claim=claim,
            evidence=evidence,
        )

        response = self.provider.generate(prompt)

        return self.parser.parse(response.content)
