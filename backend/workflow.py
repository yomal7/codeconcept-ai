from pathlib import Path

from loguru import logger
from pydantic import BaseModel

from agents.planner import PlannerAgent
from agents.reviewer import ReviewerAgent
from backend.exceptions import LLMError
from backend.jobs import create_job
from backend.models import Presentation, ReviewResult, Severity
from backend.timer import Timer
from config.settings import MAX_PLANNER_ATTEMPTS

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


def _write_json(path: Path, model: BaseModel) -> None:
    path.write_text(model.model_dump_json(indent=2), encoding="utf-8")