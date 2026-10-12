from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.analysis.repository import create_analysis_result
from app.services.llm.groq import GroqProvider
from app.services.llm.service import LLMAnalysisService
from app.services.rag.retriever import EvidenceRAGRetriever
from app.services.safety.service import SafetyService


class AnalysisService:
    def __init__(self) -> None:
        self.retriever = EvidenceRAGRetriever()
        self.llm_service = LLMAnalysisService(
            provider=GroqProvider()
        )
        self.safety_service = SafetyService()

    def analyze_claim(
        self,
        db: Session,
        claim_id: UUID,
        claim_text: str,
        top_k: int = 5,
    ):
        evidence = self.retriever.retrieve(
            db=db,
            claim_id=claim_id,
            query=claim_text,
            top_k=top_k,
        )

        verdict = self.llm_service.analyze(
            claim=claim_text,
            evidence=evidence,
        )

        safety_report = self.safety_service.validate(
            verdict=verdict,
            evidence=evidence,
        )

        if not safety_report.passed:
            raise ValueError(
                "LLM verdict failed responsible AI safety validation"
            )

        evidence_data = [
            item.model_dump(mode="json")
            for item in verdict.evidence
        ]

        return create_analysis_result(
            db=db,
            claim_id=claim_id,
            verdict=verdict.verdict.value,
            confidence=verdict.confidence,
            summary=verdict.summary,
            evidence=evidence_data,
        )
