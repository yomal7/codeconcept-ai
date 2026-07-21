from pathlib import Path

from backend.gemini_tts import GeminiTTSClient
from backend.tts_client import TTSClient


class AudioAgent:
    """Turns one slide's narration into a WAV file.

    Deliberately not a BaseAgent subclass: BaseAgent's contract is
    "text prompt in, validated pydantic model out", which doesn't fit
    audio synthesis. This gets its own equally small shape instead of
    being forced into that contract.
    """

    def __init__(self, client: TTSClient | None = None):
        self.client = client or GeminiTTSClient()

    def run(self, narration: str, out_path: Path, *, voice: str | None = None) -> Path:
        audio_bytes = self.client.synthesize(narration, voice=voice)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(audio_bytes)
        return out_path