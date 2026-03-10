from pyudskit.client import UDS


def test_encode_returns_uds_bytes_string(uds_client):
    out = uds_client.encode("Read the VIN")
    assert isinstance(out, str)


def test_encode_returns_non_empty(uds_client):
    out = uds_client.encode("Read the VIN")
    assert out != ""


def test_encode_request_returns_uds_message_object(uds_client):
    out = uds_client.encode_request("Read the VIN")
    assert out["uds_message"].__class__.__name__ == "UDSMessage"


def test_decode_returns_string(uds_client):
    out = uds_client.decode("62 F1 90")
    assert isinstance(out, str)


def test_decode_response_returns_plain_english(uds_client):
    out = uds_client.decode_response("62 F1 90")
    assert "plain_english" in out


def test_decode_dtc_status_confirmed_only(uds_client):
    flags = uds_client.decode_dtc_status(0x08)
    assert flags["confirmedDTC"] is True
    assert flags["pendingDTC"] is False


def test_read_did_vin_bytes(uds_client):
    out = uds_client.read_did(0xF190)
    assert "22 F1 90" in out["uds_bytes"]


def test_ecu_reset_hard(uds_client):
    out = uds_client.ecu_reset("hard")
    assert "11 01" in out["uds_bytes"]


def test_clear_dtcs_all(uds_client):
    out = uds_client.clear_dtcs()
    assert "14 FF FF FF" in out["uds_bytes"]


def test_tester_present_suppressed(uds_client):
    out = uds_client.tester_present()
    assert "3E 80" in out["uds_bytes"]


def test_session_history_grows(mock_llm):
    mock_llm('{"uds_bytes":"22 F1 90","service":"ReadDataByIdentifier","description":"Read VIN","plain_english":"VIN"}')
    uds = UDS(api_key="test")
    uds.ask("Q1")
    uds.ask("Q2")
    uds.ask("Q3")
    assert len(uds.session.history) == 6


def test_clear_session_resets_history(mock_llm):
    mock_llm("ok")
    uds = UDS(api_key="test")
    uds.ask("Q1")
    uds.clear_session()
    assert len(uds.session.history) == 0
