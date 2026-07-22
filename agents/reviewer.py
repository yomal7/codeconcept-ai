from agents.base import BaseAgent
from backend.models import Presentation, ReviewResult
from config.settings import GEMINI_REVIEWER_MODEL


class ReviewerAgent(BaseAgent):
    prompt_name = "reviewer"
    model_name = GEMINI_REVIEWER_MODEL

    def run(self, presentation: Presentation) -> ReviewResult:
        prompt = (
            f"{self.system_prompt}\n\n"
            "Presentation JSON to review:\n"
            f"{presentation.model_dump_json(indent=2)}"
        )
        return self.client.generate_structured(prompt, ReviewResult, model=self.model_name)