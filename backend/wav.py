import io
import wave
from pathlib import Path


def pcm_to_wav_bytes(pcm: bytes, *, channels: int = 1, rate: int = 24000, sample_width: int = 2) -> bytes:
    """Wrap raw PCM samples (what Gemini TTS returns) in a WAV container."""
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)
    return buffer.getvalue()


def wav_duration_seconds(path: Path) -> float:
    """Read a WAV file's real duration. Used so slide timing comes from the
    actual synthesized audio, not the Planner's estimated `duration` field --
    per the original design: "Duration of each audio determines slide duration."
    """
    with wave.open(str(path), "rb") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        return frames / float(rate)