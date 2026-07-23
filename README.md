# CodeConcept AI

CodeConcept AI generates short educational tech videos from a topic prompt. It uses a planner/reviewer loop to build a structured presentation, renders slides to HTML, captures screenshots, synthesizes narration audio, and assembles the final MP4 video.

## What it does

- Turns a single topic into a full presentation JSON.
- Reviews each draft with a second LLM pass before rendering.
- Renders slides with Jinja templates and CSS themes.
- Generates narration audio for each slide.
- Produces a final video under `output/`.

## Requirements

- Python 3.12 or newer.
- A Google API key in `GOOGLE_API_KEY`.
- `ffmpeg` available on your system.
- Playwright browsers installed for screenshot rendering.

## Setup

```bash
uv sync
uv run playwright install
```

If you are not using `uv`, install the dependencies from `pyproject.toml` with your preferred Python tooling.

## Configuration

Set the environment variables you need before running the pipeline. The most important one is `GOOGLE_API_KEY`.

Optional settings live in [`config/settings.py`](config/settings.py) and include:

- `GEMINI_MODEL`
- `GEMINI_PLANNER_MODEL`
- `GEMINI_REVIEWER_MODEL`
- `GEMINI_TTS_MODEL`
- `TTS_VOICE`
- `BASE_SHORT_SIDE`
- `FPS`
- `THEME`
- `LOG_LEVEL`
- `MAX_PLANNER_ATTEMPTS`
- `FFMPEG_BIN`

## Usage

Generate just the presentation JSON and review output:

```bash
uv run python scripts/generate_presentation.py --topic "Explain Kubernetes for beginners"
```

Generate the full video pipeline:

```bash
uv run python scripts/generate_video.py --topic "Explain Kubernetes for beginners"
```

The pipeline writes a job folder under `output/`, for example `output/job_YYYYMMDD_HHMMSS/`.

## Output

Each job folder contains:

- `presentation.json` - the approved presentation model.
- `review.json` - the final reviewer result.
- `slides/` - rendered slide HTML and screenshots.
- `audio/` - generated WAV narration files.
- `video/` - per-slide MP4 files and the final `final.mp4`.

## How the pipeline works

1. `PlannerAgent` turns the topic into a structured presentation.
2. `ReviewerAgent` checks the presentation for quality and correctness.
3. If the reviewer rejects it, the planner tries again with feedback.
4. Once approved, the renderer builds slide HTML and screenshots.
5. `AudioAgent` synthesizes narration for each slide.
6. The video composer combines screenshots and audio into the final MP4.

## Project structure

- `agents/` - planner, reviewer, and audio agents.
- `backend/` - LLM clients, data models, workflow, retries, timing, and WAV helpers.
- `renderer/` - HTML rendering, slide composition, screenshots, and icons.
- `templates/` - Jinja templates and CSS for slides.
- `prompts/` - system prompts for the planner and reviewer.
- `scripts/` - CLI entry points.
- `tests/` - automated tests for Gemini behavior.

## Customization

- Edit `prompts/planner.md` and `prompts/reviewer.md` to change generation or review behavior.
- Edit `templates/` and `renderer/` to change the visual style.
- Adjust `config/settings.py` or environment variables to change model selection, timing, or output settings.

## Notes

- The repository currently exposes CLI workflows rather than a web app.
- Generated artifacts are written to `output/` and are safe to inspect after each run.
