"""Command-line entry point: scrollsilo <reel-url>."""
import argparse
from pathlib import Path

from . import __version__
from .llm import DEFAULT_TEXT_MODEL, DEFAULT_VISION_MODEL
from .pipeline import process
from .transcribe import DEFAULT_WHISPER_MODEL


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="scrollsilo", description="Turn an Instagram reel into a JSON knowledge record, locally.")
    p.add_argument("url", help="public Instagram reel URL")
    p.add_argument("--out", type=Path, default=Path("output"), help="output directory (default: ./output)")
    p.add_argument("--text-model", default=DEFAULT_TEXT_MODEL, help=f"Ollama text model (default: {DEFAULT_TEXT_MODEL})")
    p.add_argument("--vision-model", default=DEFAULT_VISION_MODEL, help=f"Ollama vision model (default: {DEFAULT_VISION_MODEL})")
    p.add_argument("--whisper-model", default=DEFAULT_WHISPER_MODEL, help=f"MLX Whisper model (default: {DEFAULT_WHISPER_MODEL})")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = p.parse_args(argv)
    out = process(args.url, args.out, args.text_model, args.vision_model, args.whisper_model)
    print("wrote", out)