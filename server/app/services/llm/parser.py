import json

from pydantic import ValidationError

from app.services.llm.schemas import VerdictResponse


class LLMOutputParser:

    def parse(self, content: str) -> VerdictResponse:
        cleaned = content.strip()

        if cleaned.startswith("```"):
            lines = cleaned.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            cleaned = "\n".join(lines).strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise ValueError("LLM response is not valid JSON") from exc

        try:
            return VerdictResponse.model_validate(data)
        except ValidationError as exc:
            raise ValueError("LLM response failed verdict validation") from exc
