import subprocess
from pathlib import Path

from backend.exceptions import RenderError
from config.settings import FFMPEG_BIN, FPS


def compose_slide_video(image_path: Path, audio_path: Path, out_path: Path) -> Path:
    """PNG + WAV -> a single MP4, holding the static image for the audio's
    full duration (`-shortest` with a looped image source just means "stop
    when the audio ends", not "cut the image short").
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [
            FFMPEG_BIN, "-y",
            "-loop", "1", "-i", str(image_path),
            "-i", str(audio_path),
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-r", str(FPS),
            "-shortest",
            str(out_path),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RenderError(f"ffmpeg failed composing {out_path.name}:\n{result.stderr}")
    return out_path


def concat_videos(video_paths: list[Path], out_path: Path) -> Path:
    """Concatenate slide_00N.mp4 files (already in order) into one final.mp4.

    Uses ffmpeg's concat demuxer with `-c copy` (no re-encoding) since
    every slide video was already encoded with matching codec settings
    by compose_slide_video.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    filelist = out_path.parent / "_concat_list.txt"
    filelist.write_text(
        "\n".join(f"file '{p.resolve()}'" for p in video_paths), encoding="utf-8"
    )

    try:
        result = subprocess.run(
            [
                FFMPEG_BIN, "-y",
                "-f", "concat", "-safe", "0",
                "-i", str(filelist),
                "-c", "copy",
                str(out_path),
            ],
            capture_output=True,
            text=True,
        )
    finally:
        filelist.unlink(missing_ok=True)

    if result.returncode != 0:
        raise RenderError(f"ffmpeg concat failed:\n{result.stderr}")
    return out_path