from agents.base import BaseAgent
from backend.models import Presentation, ReviewResult


class PlannerAgent(BaseAgent):
    """Turns a topic (optionally plus reviewer feedback) into a Presentation."""

    prompt_name = "planner"

    def run(self, topic: str, feedback: ReviewResult | None = None) -> Presentation:
        prompt = f"{self.system_prompt}\n\nTopic:\n{topic}"

        if feedback is not None:
            prompt += (
                "\n\nYour previous draft was rejected by the reviewer. "
                "Fix every issue below and return a new, complete presentation "
                "(do not just patch — regenerate the full JSON):\n"
                f"{feedback.model_dump_json(indent=2)}"
            )

        return self.client.generate_structured(prompt, Presentation)