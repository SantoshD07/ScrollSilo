import json

import ollama
import pydantic
import pytest

from scrollsilo import llm


def test_analysis_rejects_too_many_tags_and_unknown_content_type():
    base = {"summary": "s", "takeaways": ["t"], "tags": ["a"], "content_type": "tutorial",
            "transcript_en": ""}
    llm.Analysis(**base)
    with pytest.raises(pydantic.ValidationError):
        llm.Analysis(**{**base, "tags": [f"t{i}" for i in range(9)]})
    with pytest.raises(pydantic.ValidationError):
        llm.Analysis(**{**base, "content_type": "promo, educational"})


def test_chat_retries_with_rising_temperature(monkeypatch):
    temps = []

    def fake_chat(options, **kwargs):
        temps.append(options["temperature"])
        assert options["num_predict"] == 50  # the token cap survives retries
        if len(temps) < 3:
            raise ollama.ResponseError("token repeat limit reached", 500)
        return {"message": {"content": "ok"}}

    monkeypatch.setattr(llm.ollama, "chat", fake_chat)
    assert llm.chat(model="m", options={"num_predict": 50})["message"]["content"] == "ok"
    assert temps == [0.0, 0.2, 0.4]


def test_chat_raises_after_last_retry(monkeypatch):
    def always_fail(**kwargs):
        raise ollama.ResponseError("boom", 500)

    monkeypatch.setattr(llm.ollama, "chat", always_fail)
    with pytest.raises(ollama.ResponseError):
        llm.chat(retries=2, model="m")


def test_analyze_parses_model_json(monkeypatch):
    payload = {"summary": "s", "takeaways": ["t"], "tags": ["python"], "content_type": "tutorial",
               "transcript_en": ""}
    monkeypatch.setattr(llm, "chat", lambda **kw: {"message": {"content": json.dumps(payload)}})
    assert llm.analyze("cap", "", ["frame"]).tags == ["python"]