from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class LLMClient(ABC):
    """Provider-agnostic contract every LLM backend must satisfy.

    Agents (Planner, Reviewer, QA, ...) depend only on this interface,
    never on a concrete provider. Swapping Gemini for OpenAI, Claude, or
    a local model means writing one new subclass of this file — nothing
    in agents/ or backend/workflow.py has to change.
    """

    @abstractmethod
    def generate_text(self, prompt: str, *, model: str | None = None) -> str:
        """Return a raw text completion for a prompt."""

    @abstractmethod
    def generate_structured(
        self,
        prompt: str,
        schema: type[T],
        *,
        model: str | None = None,
    ) -> T:
        """Return a validated instance of `schema` parsed from the model's output."""