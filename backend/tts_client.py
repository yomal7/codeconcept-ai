from abc import ABC, abstractmethod


class TTSClient(ABC):
    """Provider-agnostic contract for turning narration text into audio.

    Mirrors LLMClient: AudioAgent depends only on this interface, never
    on a concrete provider. Swapping Gemini TTS for ElevenLabs, or a
    local model, means writing one new subclass of this file.
    """

    @abstractmethod
    def synthesize(self, text: str, *, voice: str | None = None) -> bytes:
        """Return a complete WAV file (bytes) for the given narration text."""