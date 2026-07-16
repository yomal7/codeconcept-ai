from abc import ABC, abstractmethod

from backend.gemini import GeminiClient
from backend.llm_client import LLMClient
from backend.prompt_loader import load_prompt


class BaseAgent(ABC):
    """Shared plumbing for every agent.

    An agent's only job is: hold a system prompt, take some input, and
    return a validated pydantic model — using whatever LLMClient it was
    given. The client defaults to Gemini but can be swapped (tests,
    other providers) without touching subclasses.

    Subclasses set `prompt_name` to the .md file in prompts/ they use,
    e.g. `prompt_name = "planner"` loads prompts/planner.md.
    """

    prompt_name: str

    def __init__(self, client: LLMClient | None = None):
        self.client = client or GeminiClient()
        self.system_prompt = load_prompt(self.prompt_name)

    @abstractmethod
    def run(self, *args, **kwargs):
        ...
        