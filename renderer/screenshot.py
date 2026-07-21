import subprocess
from pathlib import Path

from backend.exceptions import RenderError
from config.settings import NODE_BIN, PUPPETEER_SCRIPT


def take_screenshots(slides_dir: Path, *, width: int, height: int) -> list[Path]:
    """Screenshot every slide_*.html in slides_dir to a same-named .png.

    Shells out to renderer/screenshot.js, which runs a single headless
    Chromium instance for the whole batch (via Puppeteer) rather than
    launching one per slide.
    """
    result = subprocess.run(
        [
            NODE_BIN,
            str(PUPPETEER_SCRIPT),
            "--dir", str(slides_dir),
            "--width", str(width),
            "--height", str(height),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RenderError(f"Puppeteer screenshot step failed:\n{result.stderr}")

    return sorted(slides_dir.glob("*.png"))