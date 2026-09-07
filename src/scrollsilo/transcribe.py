"""Speech-to-text with a guard that treats music and noise as 'no speech'."""
from pathlib import Path

DEFAULT_WHISPER_MODEL = "mlx-community/whisper-large-v3-turbo"
MIN_SPEECH_WORDS = 10  # fewer confident words than this is treated as music/noise, not speech


def select_speech(segments: list[dict]) -> str:
    """Join the confident segments; return '' when too few words remain to count as speech."""
    kept = [seg["text"].strip() for seg in segments
            if seg["no_speech_prob"] < 0.6 and seg["avg_logprob"] > -1.0]
    text = " ".join(t for t in kept if t)
    return text if len(text.split()) >= MIN_SPEECH_WORDS else ""


def transcribe(video: Path, model: str = DEFAULT_WHISPER_MODEL) -> tuple[str, str | None, bool]:
    """Return (transcript, language, has_speech). Transcript is empty when there is no real speech."""
    import mlx_whisper  # imported lazily: Apple-silicon only

    r = mlx_whisper.transcribe(str(video), path_or_hf_repo=model)
    text = select_speech(r["segments"])
    if not text:
        return "", None, False
    return text, r.get("language"), True