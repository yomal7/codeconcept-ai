from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "output"
PROMPTS_DIR = BASE_DIR / "prompts"
TEMPLATES_DIR = BASE_DIR / "templates"
LOGOS_DIR = BASE_DIR / "logos"
FONTS_DIR = BASE_DIR / "fonts"
MUSIC_DIR = BASE_DIR / "music"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_TTS_MODEL = os.getenv("GEMINI_TTS_MODEL", "gemini-2.5-flash-preview-tts")
TTS_VOICE = os.getenv("TTS_VOICE", "Kore")

# The long edge of a rendered slide is always BASE_SHORT_SIDE * aspect ratio,
# so a 16:9 video renders at 1920x1080 and a 9:16 video renders at
# 1080x1920 -- whatever aspect_ratio THAT video's presentation.json asked
# for, not one fixed size for every video. See renderer/dimensions.py.
BASE_SHORT_SIDE = int(os.getenv("BASE_SHORT_SIDE", 1080))
FPS = int(os.getenv("FPS", 30))

THEME = os.getenv("THEME", "codeconcept")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

MAX_PLANNER_ATTEMPTS = int(os.getenv("MAX_PLANNER_ATTEMPTS", 3))

FFMPEG_BIN = os.getenv("FFMPEG_BIN", "ffmpeg")