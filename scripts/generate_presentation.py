import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agents.planner import PlannerAgent
from backend.exceptions import GeminiRateLimitError, InvalidPresentationError
from backend.jobs import create_job


parser = argparse.ArgumentParser()

parser.add_argument(
    "--topic",
    required=True
)

args = parser.parse_args()

job = create_job()

planner = PlannerAgent()

try:
    presentation = planner.run(args.topic)
except GeminiRateLimitError as exc:
    raise SystemExit(f"Gemini API is temporarily rate-limited: {exc}") from exc
except InvalidPresentationError as exc:
    raise SystemExit(f"Planner failed to produce a valid presentation: {exc}") from exc
except Exception as exc:
    raise SystemExit(f"Presentation generation failed: {exc}") from exc

(job / "presentation.json").write_text(
    presentation.model_dump_json(indent=2),
    encoding="utf-8"
)

print(f"Saved to {job}")