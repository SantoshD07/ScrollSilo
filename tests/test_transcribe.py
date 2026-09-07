from scrollsilo.transcribe import select_speech


def seg(text, nsp=0.0, lp=-0.2):
    return {"text": text, "no_speech_prob": nsp, "avg_logprob": lp}


def test_music_snippet_is_not_speech():
    # Four confident words are below the 10-word threshold.
    assert select_speech([seg("Calling you to say", lp=-0.51)]) == ""


def test_confident_speech_is_kept():
    text = "this is a long enough sentence to count as real spoken words today"
    assert select_speech([seg(text)]) == text


def test_hindi_segment_with_high_compression_ratio_is_kept():
    # Devanagari trips Whisper's English-tuned compression_ratio check; it must not be filtered.
    hindi = "क्या आप लोग को आइडिया है कि आप पाइथन सीख के क्या क्या कर सकते हैं"
    s = {**seg(hindi, lp=-0.17), "compression_ratio": 2.73}
    assert select_speech([s]) == hindi


def test_low_confidence_and_no_speech_segments_are_dropped():
    good = "one two three four five six seven eight nine ten eleven"
    segs = [seg("noise noise noise", nsp=0.9), seg("garbled words here", lp=-1.5), seg(good)]
    assert select_speech(segs) == good