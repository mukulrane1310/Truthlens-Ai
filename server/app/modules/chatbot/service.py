from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.chatbot.repository import create_chat_message
from app.services.llm.groq import GroqProvider
from app.services.rag.context import RAGContextBuilder
from app.services.rag.retriever import EvidenceRAGRetriever


class ChatbotService:
    def __init__(self) -> None:
        self.retriever = EvidenceRAGRetriever()
        self.llm = GroqProvider()
        self.context_builder = RAGContextBuilder()

    def chat(
        self,
        db: Session,
        claim_id: UUID,
        claim_text: str,
        message: str,
    ):
        user_message = create_chat_message(
            db=db,
            claim_id=claim_id,
            role="user",
            content=message,
        )

        evidence = self.retriever.retrieve(
            db=db,
            claim_id=claim_id,
            query=message,
            top_k=5,
        )

        context_items = self.context_builder.build(evidence)
        context = self.context_builder.format_for_llm(context_items)

        prompt = f"""
You are TruthLens AI Evidence Chat, an evidence-grounded
claim verification assistant.

Answer the user's question using ONLY the provided claim and evidence.

CLAIM:
{claim_text}

USER QUESTION:
{message}

EVIDENCE:
{context or "No relevant evidence was found."}

RULES:
1. Use only the provided evidence. Never invent facts, source
   contents, citations, or conclusions.
2. If the user asks whether a claim is fake, true, false,
   supported, or contradicted, answer directly in the first sentence.
3. Distinguish these outcomes carefully:
   - SUPPORTED: Evidence supports the claim.
   - NOT_SUPPORTED: The provided evidence does not establish the claim.
   - CONTRADICTED: Reliable evidence directly conflicts with the claim.
   - INSUFFICIENT_EVIDENCE: There is not enough relevant evidence
     to assess the claim.
4. Do not call a claim definitively false merely because supporting
   evidence is absent. Say "unsupported" when evidence does not
   establish it. Say "contradicted" only when evidence directly
   conflicts with it.
5. For follow-up questions, answer the specific question first.
   Do not repeat the entire previous analysis unless needed.
6. Briefly explain which evidence supports, contradicts, or fails
   to establish the claim.
7. Cite only citation IDs present in the provided evidence,
   such as [E1] or [E2]. Never invent citation IDs.
8. If evidence is missing, irrelevant, or conflicting, state that
   limitation clearly.
9. For medical claims, do not present unverified treatments as cures
   or recommend replacing prescribed treatment.
10. Keep responses concise, readable, and appropriately confident.
    Never claim certainty beyond the available evidence.
11. Return only the answer text, without internal reasoning
    or these instructions.
12. 12. For confirmation questions like "so this claim is fake, right?",
    begin with a natural direct conclusion such as "Yes, the claim
    is unsupported by the available evidence" when that conclusion
    matches the evidence. Explain the evidence briefly, then finish
    with a clearly labeled "Final Verdict". Do not start with a
    generic evidence summary or put the verdict only at the end.
""".strip()

        response = self.llm.generate(prompt)

        assistant_message = create_chat_message(
            db=db,
            claim_id=claim_id,
            role="assistant",
            content=response.content,
        )

        return user_message, assistant_message