"""The end-to-end pipeline for one reel."""
import json
from pathlib import Path

from .download import download
from .frames import clean_frame_notes, extract_frames
from .llm import DEFAULT_TEXT_MODEL, DEFAULT_VISION_MODEL, analyze, describe_frames
from .record import build_record
from .transcribe import DEFAULT_WHISPER_MODEL, transcribe


def process(url: str, out_dir: Path, text_model: str = DEFAULT_TEXT_MODEL,
            vision_model: str = DEFAULT_VISION_MODEL,
            whisper_model: str = DEFAULT_WHISPER_MODEL) -> Path:
    """Download, transcribe, look at frames, analyze, and write <out_dir>/<id>.json."""
    out_dir.mkdir(parents=True, exist_ok=True)
    print("downloading...")
    video, info = download(url, out_dir / ".media")
    print("transcribing...")
    transcript, language, has_speech = transcribe(video, whisper_model)
    print("sampling frames + vision...")
    frame_notes = clean_frame_notes(describe_frames(extract_frames(video), vision_model))
    print("tagging...")
    analysis = analyze(info.get("description") or "", transcript, frame_notes, text_model)
    record = build_record(url, info, transcript, language, has_speech, analysis)
    out = out_dir / f"{info['id']}.json"
    out.write_text(json.dumps(record, indent=2, ensure_ascii=False))
    return out