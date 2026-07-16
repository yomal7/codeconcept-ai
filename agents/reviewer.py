from agents.base import BaseAgent
from backend.models import Presentation, ReviewResult


class ReviewerAgent(BaseAgent):
    """Validates a Presentation for correctness, pacing, and clarity."""

    prompt_name = "reviewer"

    def run(self, presentation: Presentation) -> ReviewResult:
        prompt = (
            f"{self.system_prompt}\n\n"
            "Presentation JSON to review:\n"
            f"{presentation.model_dump_json(indent=2)}"
        )
        return self.client.generate_structured(prompt, ReviewResult)