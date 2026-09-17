"""Local model calls through Ollama: frame descriptions and the structured analysis."""
import base64
from pathlib import Path
from typing import Literal

import ollama
from pydantic import BaseModel, Field

DEFAULT_TEXT_MODEL = "qwen2.5:7b"
DEFAULT_VISION_MODEL = "qwen2.5vl:7b"

ContentType = Literal["tutorial", "opinion", "news", "entertainment", "promo", "personal", "other"]


class Analysis(BaseModel):
    summary: str = Field(description="2-3 sentences in English on the knowledge/message conveyed; ignore appearance and setting")
    takeaways: list[str] = Field(max_length=6, description="Concrete, self-contained points worth remembering")
    tags: list[str] = Field(max_length=8, description="3-8 lowercase kebab-case topic tags; no creator, brand or clothing tags")
    content_type: ContentType
    transcript_en: str = Field(description="English translation of the transcript; empty string if no speech")


def chat(retries: int = 3, **kwargs):
    """ollama.chat with a capped output length; retry with rising temperature on loops/errors."""
    base = kwargs.pop("options", {})
    for attempt in range(retries):
        opts = {**base, "temperature": 0.2 * attempt}
        try:
            return ollama.chat(options=opts, **kwargs)
        except ollama.ResponseError as e:
            print(f"  ollama error ({e.status_code}), retry {attempt + 1}/{retries}")
            if attempt == retries - 1:
                raise


def describe_frames(frames: list[Path], model: str = DEFAULT_VISION_MODEL) -> list[str]:
    notes = []
    for f in frames:
        r = chat(model=model, options={"num_predict": 200}, messages=[{
            "role": "user",
            "content": "Transcribe any on-screen text verbatim, one line per item, after 'TEXT:'. "
                       "Before that, in one short sentence, say what is shown (ignore clothing and decor). "
                       "If there is no on-screen text write 'TEXT: none'.",
            "images": [base64.b64encode(f.read_bytes()).decode()],
        }])
        notes.append(r["message"]["content"].strip())
    return notes


def analyze(caption: str, transcript: str, frame_notes: list[str],
            model: str = DEFAULT_TEXT_MODEL) -> Analysis:
    prompt = (
        "You are building a personal knowledge base from saved Instagram reels. Extract the KNOWLEDGE "
        "the reel conveys. The transcript and caption are the primary sources; frame notes only add "
        "on-screen text and context. Never describe the person's appearance, clothing or room. "
        "If the reel is mostly promotion, say so briefly and capture only the real information in it. "
        "The transcript may be in any language; write all output in English.\n"
        f"CAPTION:\n{caption}\n\nTRANSCRIPT:\n{transcript or '(no speech)'}\n\n"
        "FRAME NOTES:\n" + "\n".join(f"- {n}" for n in frame_notes)
    )
    r = chat(model=model, messages=[{"role": "user", "content": prompt}],
             format=Analysis.model_json_schema(), options={"num_predict": 1500})
    return Analysis.model_validate_json(r["message"]["content"])