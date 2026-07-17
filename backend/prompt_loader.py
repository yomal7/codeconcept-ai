from pathlib import Path

from config.settings import PROMPTS_DIR


def load_prompt(name: str) -> str:
    path = PROMPTS_DIR / f"{name}.md"

    return path.read_text(encoding="utf-8")