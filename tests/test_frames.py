from scrollsilo.frames import clean_frame_notes


def test_inlines_on_screen_text():
    notes = ["A diagram is shown. TEXT: LLM vs RAG\nAI Agent"]
    assert clean_frame_notes(notes) == ["A diagram is shown. [on-screen: LLM vs RAG | AI Agent]"]


def test_drops_text_none_and_empty_descriptions():
    assert clean_frame_notes(["A person talks. TEXT: none", "TEXT: orphan text"]) == ["A person talks."]


def test_drops_exact_repeats():
    n = "A slide. TEXT: Hello"
    assert clean_frame_notes([n, n, n]) == ["A slide. [on-screen: Hello]"]