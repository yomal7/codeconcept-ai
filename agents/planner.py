import json

from agents.base import BaseAgent
from backend.exceptions import InvalidPresentationError
from backend.models import Presentation
from backend.prompt_loader import load_prompt


class PlannerAgent(BaseAgent):

    def __init__(self):

        super().__init__()

        self.system_prompt = load_prompt("planner")

    def run(self, topic: str) -> Presentation:

        prompt = f"""
{self.system_prompt}

Topic:

{topic}
"""

        presentation = self.client.generate(
            prompt,
            response_schema=Presentation,
        )

        if isinstance(presentation, Presentation):
            return presentation

        if isinstance(presentation, dict):
            return Presentation.model_validate(presentation)

        if isinstance(presentation, str):
            try:
                payload = json.loads(presentation)
            except json.JSONDecodeError as exc:
                raise InvalidPresentationError("Planner returned invalid JSON") from exc

            return Presentation.model_validate(payload)

        raise InvalidPresentationError("Planner returned an unexpected payload")