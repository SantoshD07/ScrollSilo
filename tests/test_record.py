from scrollsilo.llm import Analysis
from scrollsilo.record import build_record, parse_hashtags, posted_iso

ANALYSIS = Analysis(summary="s", takeaways=["t"], tags=["python"], content_type="tutorial",
                    transcript_en="model invented this")
INFO = {"uploader": "Example Creator", "channel": "example_creator", "uploader_id": "123",
        "upload_date": "20260919", "description": "Learn Python #Python #python #AI"}


def test_parse_hashtags_lowercases_and_dedupes():
    assert parse_hashtags("Learn #Python and #python plus #AI") == ["python", "ai"]


def test_parse_hashtags_ignores_bracketed_keyword_lists():
    assert parse_hashtags("[dataanalytics, deeplearning] #genai") == ["genai"]


def test_parse_hashtags_handles_empty():
    assert parse_hashtags("") == [] and parse_hashtags(None) == []


def test_posted_iso():
    assert posted_iso({"upload_date": "20260919"}) == "2026-09-19"
    assert posted_iso({}) is None
    assert posted_iso({"upload_date": "2026"}) is None


def test_build_record_has_all_fields_and_prefers_channel_handle():
    r = build_record("https://example.com/reel/x", INFO, "hello world", "en", True, ANALYSIS)
    assert r["source"] == "https://example.com/reel/x"
    assert r["handle"] == "example_creator"
    assert r["posted"] == "2026-09-19"
    assert r["hashtags"] == ["python", "ai"]
    assert r["has_speech"] is True and r["transcript"] == "hello world"
    assert r["transcript_en"] == "model invented this"


def test_build_record_empties_translation_when_no_speech():
    r = build_record("u", INFO, "", None, False, ANALYSIS)
    assert r["has_speech"] is False
    assert r["transcript"] == "" and r["transcript_en"] == "" and r["language"] is None