# Contributing

Thanks for helping out. ScrollSilo is a small project, so the process is light.

## Setup

```bash
brew install ffmpeg yt-dlp
uv sync --extra dev
```

## Checks

Run both before opening a pull request:

```bash
uv run ruff check .
uv run pytest
```

The tests use stubs and never call Instagram, Ollama or Whisper, so they run on any platform.

## Guidelines

- Keep changes small and focused on one thing.
- Add or update a test for behaviour you change.
- Don't commit downloaded media, run output, or other people's captions and transcripts. Use synthetic examples.
- Describe user-visible changes in `CHANGELOG.md` under "Unreleased".