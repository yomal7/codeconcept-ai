import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.exceptions import LLMError, RenderError
from backend.workflow import run_pipeline

parser = argparse.ArgumentParser()
parser.add_argument("--topic", required=True)
args = parser.parse_args()

try:
    job_dir, final_video = run_pipeline(args.topic)
except LLMError as exc:
    raise SystemExit(f"Presentation generation failed: {exc}") from exc
except RenderError as exc:
    raise SystemExit(f"Rendering failed: {exc}") from exc

print(f"Video ready: {final_video}")
print(f"Full job folder: {job_dir}")