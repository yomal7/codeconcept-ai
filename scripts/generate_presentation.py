import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.exceptions import LLMError
from backend.workflow import run_planning_stage

parser = argparse.ArgumentParser()
parser.add_argument("--topic", required=True)
args = parser.parse_args()

try:
    presentation, review, job_dir = run_planning_stage(args.topic)
except LLMError as exc:
    raise SystemExit(f"Presentation generation failed: {exc}") from exc

print(f"Approved presentation saved to {job_dir}")
print(f"  presentation.json  ({len(presentation.slides)} slides)")
print(f"  review.json         (approved={review.approved})")