from pathlib import Path

from loguru import logger
from pydantic import BaseModel

from agents.audio import AudioAgent
from agents.planner import PlannerAgent
from agents.reviewer import ReviewerAgent
from backend.exceptions import LLMError
from backend.jobs import create_job
from backend.models import Presentation, ReviewResult, Severity
from backend.timer import Timer
from config.settings import MAX_PLANNER_ATTEMPTS
from renderer.composer import compose_slide_video, concat_videos
from renderer.dimensions import resolve_dimensions
from renderer.html_renderer import HTMLRenderer
from renderer.screenshot import take_screenshots


def is_approved(review: ReviewResult) -> bool:
    for issue in review.issues:
        if issue.severity in (Severity.MAJOR, Severity.CRITICAL):
            return False
    return True


def run_planning_stage(topic: str, job_dir: Path | None = None) -> tuple[Presentation, ReviewResult, Path]:
    """Planner -> Reviewer loop.

    Writes presentation.json and review.json into the job folder after
    every attempt (so a failed run is still fully debuggable), and
    returns as soon as the reviewer approves. Raises LLMError if no
    attempt is approved within MAX_PLANNER_ATTEMPTS.
    """
    job_dir = job_dir or create_job()
    planner = PlannerAgent()
    reviewer = ReviewerAgent()

    feedback: ReviewResult | None = None
    planner_runs = 0
    reviewer_runs = 0

    for attempt in range(1, MAX_PLANNER_ATTEMPTS + 1):
        logger.info(f"[{job_dir.name}] planner attempt {attempt}/{MAX_PLANNER_ATTEMPTS}")

        planner_runs += 1
        with Timer() as planner_timer:
            presentation = planner.run(topic, feedback=feedback)
        logger.info(
            f"[{job_dir.name}] planner run #{planner_runs} completed in {planner_timer.elapsed:.2f}s"
        )

        reviewer_runs += 1
        with Timer() as reviewer_timer:
            review = reviewer.run(presentation)
        logger.info(
            f"[{job_dir.name}] reviewer run #{reviewer_runs} completed in {reviewer_timer.elapsed:.2f}s"
        )

        _write_json(job_dir / "presentation.json", presentation)
        _write_json(job_dir / "review.json", review)

        approved = is_approved(review)

        if review.approved and approved:
            logger.info(f"[{job_dir.name}] approved on attempt {attempt}")
            return presentation, review, job_dir

        logger.warning(f"[{job_dir.name}] rejected on attempt {attempt}: {review.summary}")
        feedback = review

    raise LLMError(
        f"Planner could not produce an approved presentation after {MAX_PLANNER_ATTEMPTS} attempts"
    )


def run_rendering_stage(presentation: Presentation, job_dir: Path) -> Path:
    """Approved Presentation -> HTML -> PNG -> WAV -> per-slide MP4 -> final.mp4.

    Slide video duration always comes from the ACTUAL synthesized audio
    length (read back off the .wav file), never from the Planner's
    estimated `duration` field -- that field is only a hint the Planner
    uses to pace narration while writing, per the original design:
    "Duration of each audio determines slide duration."
    """
    width, height = resolve_dimensions(presentation.video.aspect_ratio)

    logger.info(f"[{job_dir.name}] rendering {len(presentation.slides)} HTML slides")
    HTMLRenderer().render(presentation, job_dir)

    logger.info(f"[{job_dir.name}] screenshotting slides with Puppeteer ({width}x{height})")
    take_screenshots(job_dir / "slides", width=width, height=height)

    audio_agent = AudioAgent()
    slide_videos: list[Path] = []

    for slide in presentation.slides:
        audio_path = job_dir / "audio" / f"slide_{slide.id:03d}.wav"
        with Timer() as audio_timer:
            audio_agent.run(slide.narration, audio_path)
        logger.info(f"[{job_dir.name}] slide {slide.id} audio synthesized in {audio_timer.elapsed:.2f}s")

        png_path = job_dir / "slides" / f"slide_{slide.id:03d}.png"
        video_path = job_dir / "video" / f"slide_{slide.id:03d}.mp4"
        compose_slide_video(png_path, audio_path, video_path)
        slide_videos.append(video_path)

    logger.info(f"[{job_dir.name}] merging {len(slide_videos)} slide videos")
    final_path = concat_videos(slide_videos, job_dir / "video" / "final.mp4")
    logger.info(f"[{job_dir.name}] done -> {final_path}")
    return final_path


def run_pipeline(topic: str) -> tuple[Path, Path]:
    """Full Topic -> final.mp4 pipeline. Returns (job_dir, final_video_path)."""
    presentation, _review, job_dir = run_planning_stage(topic)
    final_video = run_rendering_stage(presentation, job_dir)
    return job_dir, final_video


def _write_json(path: Path, model: BaseModel) -> None:
    path.write_text(model.model_dump_json(indent=2), encoding="utf-8")