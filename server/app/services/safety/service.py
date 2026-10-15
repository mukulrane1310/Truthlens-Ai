
from app.services.llm.schemas import Verdict, VerdictResponse
from app.services.rag.context import RAGContextBuilder
from app.services.rag.interface import RetrievedEvidence
from app.services.safety.schemas import SafetyCheckResult, SafetyReport


class SafetyService:
    def validate(
        self,
        verdict: VerdictResponse,
        evidence: list[RetrievedEvidence],
    ) -> SafetyReport:
        context_items = RAGContextBuilder().build(evidence)
        evidence_ids = {item.citation_id for item in context_items}

        grounded = SafetyCheckResult(
            passed=bool(evidence) or verdict.verdict == Verdict.INSUFFICIENT_EVIDENCE,
            reason=(
                "Verdict has available evidence."
                if evidence
                else "No evidence was available; insufficient evidence is required."
            ),
        )

        citation_ids = {
            item.citation_id
            for item in verdict.evidence
        }

        citations_valid = SafetyCheckResult(
            passed=citation_ids.issubset(evidence_ids),
            reason=(
                "All citations reference retrieved evidence."
                if citation_ids.issubset(evidence_ids)
                else "One or more citations do not reference retrieved evidence."
            ),
        )

        confidence_valid = SafetyCheckResult(
            passed=0.0 <= verdict.confidence <= 1.0,
            reason="Confidence is within the valid range.",
        )

        strong_verdicts = {
            Verdict.SUPPORTED,
            Verdict.PARTIALLY_SUPPORTED,
            Verdict.MIXED_EVIDENCE,
            Verdict.NOT_SUPPORTED,
        }

        verdict_safe = SafetyCheckResult(
            passed=bool(evidence) or verdict.verdict not in strong_verdicts,
            reason=(
                "Verdict is supported by available evidence."
                if evidence
                else "Strong verdicts require supporting evidence."
            ),
        )

        return SafetyReport(
            grounded=grounded,
            citations_valid=citations_valid,
            confidence_valid=confidence_valid,
            verdict_safe=verdict_safe,
        )
