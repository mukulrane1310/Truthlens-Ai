from app.services.rag.interface import RetrievedEvidence
from app.services.rag.context import RAGContextBuilder


class TruthLensPromptBuilder:

    def __init__(self) -> None:
        self.context_builder = RAGContextBuilder()

    def build(
        self,
        claim: str,
        evidence: list[RetrievedEvidence],
    ) -> str:
        context_items = self.context_builder.build(evidence)
        context = self.context_builder.format_for_llm(context_items)

        return f"""
You are TruthLens AI, an evidence-grounded claim verification system.

Your task is to evaluate the user's claim using ONLY the provided evidence.

USER CLAIM:
{claim}

EVIDENCE:
{context or "No evidence was retrieved."}

RULES:
1. Do not use outside knowledge.
2. Do not invent facts, sources, or citations.
3. Classify each relevant evidence item as SUPPORTING, CONTRADICTING, or NEUTRAL.
4. Use the citation IDs exactly as provided, such as E1, E2.
5. If evidence conflicts, use MIXED_EVIDENCE when appropriate.
6. If evidence only supports part of the claim, use PARTIALLY_SUPPORTED.
7. If evidence is insufficient, use INSUFFICIENT_EVIDENCE.
8. Confidence must be a number between 0 and 1.
9. Keep the summary concise and evidence-grounded.
10. Return ONLY valid JSON. Do not use markdown fences.

Required JSON format:
{{
  "verdict": "SUPPORTED | PARTIALLY_SUPPORTED | MIXED_EVIDENCE | NOT_SUPPORTED | INSUFFICIENT_EVIDENCE",
  "confidence": 0.0,
  "summary": "Brief evidence-grounded explanation.",
  "evidence": [
    {{
      "citation_id": "E1",
      "classification": "SUPPORTING | CONTRADICTING | NEUTRAL",
      "reasoning": "Why this evidence supports the classification."
    }}
  ]
}}
""".strip()
