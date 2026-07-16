from pathlib import Path
from datetime import datetime

from config.settings import OUTPUT_DIR


def create_job():

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    job = OUTPUT_DIR / f"job_{timestamp}"

    job.mkdir(parents=True)

    return job