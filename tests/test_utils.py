import pytest

from pyuds.utils import (
    parse_hex,
    extract_json,
    build_alfid,
    split_dtc,
    dtc_status_summary,
    suppress_pos_rsp,
    positive_response_sid,
)


def test_parse_hex_with_spaces():
    assert parse_hex("22 F1 90") == b"\x22\xF1\x90"


def test_parse_hex_without_spaces():
    assert parse_hex("22F190") == b"\x22\xF1\x90"


def test_parse_hex_invalid_raises():
    with pytest.raises(ValueError):
        parse_hex("ZZ")


def test_extract_json_from_raw():
    data = extract_json('{"a":1}')
    assert data["a"] == 1


def test_extract_json_from_fenced_markdown():
    data = extract_json("```json\n{\"a\":2}\n```")
    assert data["a"] == 2


def test_extract_json_from_prose():
    data = extract_json("hello {\"a\":3} world")
    assert data["a"] == 3


def test_build_alfid_4_byte_addr_1_byte_size():
    assert build_alfid(4, 1) == 0x41


def test_split_dtc_powertrain():
    cat, code = split_dtc(b"\x01\x23\x45")
    assert cat == "P"
    assert code.startswith("P")


def test_dtc_status_summary_multiple_flags():
    summary = dtc_status_summary(0x2C)
    assert "pendingDTC" in summary
    assert "confirmedDTC" in summary


def test_suppress_pos_rsp_sets_bit7():
    assert suppress_pos_rsp(0x00) == 0x80


def test_positive_response_sid():
    assert positive_response_sid(0x22) == 0x62
