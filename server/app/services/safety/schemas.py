from pydantic import BaseModel, Field


class SafetyCheckResult(BaseModel):
    passed: bool
    reason: str = Field(min_length=1)


class SafetyReport(BaseModel):
    grounded: SafetyCheckResult
    citations_valid: SafetyCheckResult
    confidence_valid: SafetyCheckResult
    verdict_safe: SafetyCheckResult

    @property
    def passed(self) -> bool:
        return all(
            [
                self.grounded.passed,
                self.citations_valid.passed,
                self.confidence_valid.passed,
                self.verdict_safe.passed,
            ]
        )
