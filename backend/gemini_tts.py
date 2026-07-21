from google import genai
from google.genai import types

from backend.exceptions import LLMGenerationError, LLMRateLimitError
from backend.gemini_errors import is_rate_limit
from backend.retry import call_with_retry
from backend.tts_client import TTSClient
from backend.wav import pcm_to_wav_bytes
from config.settings import GEMINI_TTS_MODEL, GOOGLE_API_KEY, TTS_VOICE


class GeminiTTSClient(TTSClient):
    """Google Gemini TTS implementation of the TTSClient contract."""

    def __init__(self):
        self._client = genai.Client(api_key=GOOGLE_API_KEY)

    def synthesize(self, text: str, *, voice: str | None = None) -> bytes:
        response = self._call(text, voice=voice or TTS_VOICE)
        pcm = self._extract_pcm(response)
        return pcm_to_wav_bytes(pcm)

    # ---- internals ---------------------------------------------------

    def _call(self, text: str, *, voice: str):
        config = types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice)
                )
            ),
        )
        try:
            return call_with_retry(
                lambda: self._client.models.generate_content(
                    model=GEMINI_TTS_MODEL,
                    contents=text,
                    config=config,
                ),
                is_retryable=is_rate_limit,
            )
        except Exception as exc:
            if is_rate_limit(exc):
                raise LLMRateLimitError("Gemini TTS is temporarily rate-limited. Please retry shortly.") from exc
            raise LLMGenerationError(f"Gemini TTS failed: {exc}") from exc

    def _extract_pcm(self, response) -> bytes:
        try:
            return response.candidates[0].content.parts[0].inline_data.data
        except (IndexError, AttributeError) as exc:
            # Documented Gemini TTS quirk: it occasionally returns text
            # tokens instead of audio tokens. Treat it as a generation
            # failure so the caller's retry loop can try again.
            raise LLMGenerationError("Gemini TTS returned no audio data") from exc