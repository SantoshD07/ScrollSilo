import json

from scrollsilo import pipeline
from scrollsilo.llm import Analysis

INFO = {"id": "abc123", "uploader": "Example Creator", "channel": "example_creator",
        "upload_date": "20260919", "description": "A caption #python"}
ANALYSIS = Analysis(summary="s", takeaways=["t"], tags=["python"], content_type="tutorial",
                    transcript_en="invented")


def stub(monkeypatch, tmp_path, transcribe_result):
    monkeypatch.setattr(pipeline, "download", lambda url, media: (tmp_path / "abc123.mp4", INFO))
    monkeypatch.setattr(pipeline, "transcribe", lambda video, model: transcribe_result)
    monkeypatch.setattr(pipeline, "extract_frames", lambda video: [tmp_path / "f.jpg"])
    monkeypatch.setattr(pipeline, "describe_frames", lambda frames, model: ["A slide. TEXT: Hi"])
    monkeypatch.setattr(pipeline, "analyze", lambda cap, tr, notes, model: ANALYSIS)


def test_process_writes_json_named_after_reel_id(monkeypatch, tmp_path):
    stub(monkeypatch, tmp_path, ("hello there", "en", True))
    out = pipeline.process("https://www.instagram.com/reel/abc123/", tmp_path / "out")
    assert out == tmp_path / "out" / "abc123.json"
    rec = json.loads(out.read_text())
    assert rec["source"] == "https://www.instagram.com/reel/abc123/"
    assert rec["hashtags"] == ["python"] and rec["has_speech"] is True


def test_process_leaves_transcript_empty_without_speech(monkeypatch, tmp_path):
    stub(monkeypatch, tmp_path, ("", None, False))
    rec = json.loads(pipeline.process("u", tmp_path / "out").read_text())
    assert rec["has_speech"] is False and rec["transcript"] == "" and rec["transcript_en"] == ""