from pyudskit.transport.isotp import IsoTpReassembler, IsoTpSegmenter


def test_isotp_single_frame_roundtrip():
    payload = b"\x22\xF1\x90"
    seg = IsoTpSegmenter()
    frames = seg.segment(payload)
    assert len(frames) == 1
    r = IsoTpReassembler()
    out = r.feed(frames[0])
    assert out == payload


def test_isotp_multi_frame_roundtrip():
    payload = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B"
    seg = IsoTpSegmenter()
    frames = seg.segment(payload)
    r = IsoTpReassembler()
    out = None
    for f in frames:
        out = r.feed(f) or out
    assert out == payload
