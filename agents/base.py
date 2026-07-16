from abc import ABC, abstractmethod

from backend.gemini import GeminiClient


class BaseAgent(ABC):

    def __init__(self):

        self.client = GeminiClient()

    @abstractmethod
    def run(self, *args, **kwargs):
        pass