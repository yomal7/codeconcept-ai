from pathlib import Path

from playwright.sync_api import sync_playwright

from backend.exceptions import RenderError


def take_screenshots(slides_dir: Path, *, width: int, height: int) -> list[Path]:
    """Screenshot every slide_*.html in slides_dir to a same-named .png.

    Pure Python (Playwright), no Node/npm involved. Runs a single headless
    Chromium instance for the whole batch instead of launching one per
    slide.
    """
    html_files = sorted(slides_dir.glob("slide_*.html"))
    if not html_files:
        raise RenderError(f"No slide_*.html files found in {slides_dir}")

    png_paths: list[Path] = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            try:
                for html_file in html_files:
                    page = browser.new_page(viewport={"width": width, "height": height})
                    page.goto(f"file://{html_file.resolve()}")
                    png_path = html_file.with_suffix(".png")
                    page.screenshot(path=str(png_path))
                    page.close()
                    png_paths.append(png_path)
            finally:
                browser.close()
    except Exception as exc:
        raise RenderError(f"Screenshot step failed: {exc}") from exc

    return png_paths