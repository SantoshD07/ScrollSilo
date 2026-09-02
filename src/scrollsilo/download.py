"""Fetch a reel and its metadata with yt-dlp."""
import json
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> str:
    r = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"{cmd[0]} failed (exit {r.returncode}): {r.stderr.strip()}")
    return r.stdout


def download(url: str, media_dir: Path) -> tuple[Path, dict]:
    media_dir.mkdir(parents=True, exist_ok=True)
    out = media_dir / "%(id)s.%(ext)s"
    info = json.loads(run(["yt-dlp", "--no-playlist", "-f", "mp4/best", "-o", str(out),
                           "--print-json", "--no-simulate", url]))
    return media_dir / f"{info['id']}.{info['ext']}", info