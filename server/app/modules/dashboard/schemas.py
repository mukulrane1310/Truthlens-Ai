from pydantic import BaseModel


class VerdictStats(BaseModel):
    supported: int = 0
    partially_supported: int = 0
    mixed_evidence: int = 0
    not_supported: int = 0
    insufficient_evidence: int = 0


class DashboardSummary(BaseModel):
    total_claims: int
    total_analyses: int
    total_web_sources: int
    total_uploaded_sources: int
    verdicts: VerdictStats
