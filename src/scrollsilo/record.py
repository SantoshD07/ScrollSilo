"""Assemble the final JSON record for a reel."""
import re

from .llm import Analysis


def parse_hashtags(caption: str) -> list[str]:
    seen = []
    for h in re.findall(r"#(\w+)", caption or ""):
        h = h.lower()
        if h not in seen:
            seen.append(h)
    return seen


def posted_iso(info: dict) -> str | None:
    d = info.get("upload_date")
    return f"{d[:4]}-{d[4:6]}-{d[6:]}" if d and len(d) == 8 else None


def build_record(url: str, info: dict, transcript: str, language: str | None,
                 has_speech: bool, analysis: Analysis) -> dict:
    caption = info.get("description") or ""
    record = {
        "source": url,
        "creator": info.get("uploader"),
        "handle": info.get("channel") or info.get("uploader_id"),
        "posted": posted_iso(info),
        "caption": caption,
        "hashtags": parse_hashtags(caption),
        "has_speech": has_speech,
        "language": language,
        "transcript": transcript,
        **analysis.model_dump(),
    }
    if not has_speech:
        record["transcript_en"] = ""  # never let the model invent a transcript from the caption
    return record