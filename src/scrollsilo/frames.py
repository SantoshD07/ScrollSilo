"""Sample frames from a video with ffmpeg and tidy the vision model's notes."""
from pathlib import Path

from .download import run

N_FRAMES = 6


def extract_frames(video: Path, n_frames: int = N_FRAMES) -> list[Path]:
    duration = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(video)]))
    frames = []
    for i in range(n_frames):
        t = duration * (i + 0.5) / n_frames
        f = video.with_name(f"{video.stem}_f{i}.jpg")
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(video),
             "-frames:v", "1", "-vf", "scale=768:-1", str(f)])
        frames.append(f)
    return frames


def clean_frame_notes(notes: list[str]) -> list[str]:
    """Flatten to one line each, drop 'TEXT: none'/empty, and drop exact repeats."""
    seen, out = set(), []
    for n in notes:
        desc, _, text = n.partition("TEXT:")
        desc = " ".join(desc.split())
        text = " | ".join(t.strip() for t in text.splitlines() if t.strip() and t.strip().lower() != "none")
        line = desc + (f" [on-screen: {text}]" if text else "")
        if desc and line not in seen:
            seen.add(line)
            out.append(line)
    return out