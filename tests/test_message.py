from pyudskit.message import UDSMessage


def test_from_hex_strips_spaces():
    msg = UDSMessage.from_hex("22 F1 90")
    assert msg.raw_bytes == b"\x22\xF1\x90"


def test_from_hex_handles_0x_prefix():
    msg = UDSMessage.from_hex("0x22F190")
    assert msg.raw_bytes == b"\x22\xF1\x90"


def test_positive_response_detection():
    msg = UDSMessage.from_hex("50 03 00 19 01 F4")
    assert msg.is_positive_response is True


def test_negative_response_detection():
    msg = UDSMessage.from_hex("7F 22 31")
    assert msg.is_negative_response is True


def test_nrc_extraction():
    msg = UDSMessage.from_hex("7F 22 31")
    assert msg.nrc == 0x31


def test_request_service_id_from_positive():
    msg = UDSMessage.from_hex("62 F1 90")
    assert msg.request_service_id == 0x22


def test_service_name_with_response_tag():
    msg = UDSMessage.from_hex("62 F1 90")
    assert "Positive Response" in msg.service_name


def test_dtc_status_decode_confirmed():
    msg = UDSMessage.from_hex("19 02 08")
    flags = msg.decode_dtc_status(0x08)
    assert flags == ["confirmedDTC"]


def test_dtc_status_decode_multiple_bits():
    msg = UDSMessage.from_hex("19 02 2C")
    flags = msg.decode_dtc_status(0x2C)
    assert set(flags) == {"pendingDTC", "confirmedDTC", "testFailedSinceLastClear"}


def test_validate_empty_bytes():
    msg = UDSMessage.from_bytes(b"")
    valid, reason = msg.validate()
    assert valid is False
    assert reason == "empty PDU"


def test_to_hex_default_separator():
    msg = UDSMessage.from_hex("22 F1 90")
    assert msg.to_hex() == "22 F1 90"


def test_to_hex_no_separator():
    msg = UDSMessage.from_hex("22 F1 90")
    assert msg.to_hex(sep="") == "22F190"
