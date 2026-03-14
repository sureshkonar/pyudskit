from pyudskit.transport.mock import MockTransport
from pyudskit.transport.session import UDSTransportClient, UDSTiming


def test_transport_client_basic():
    tr = MockTransport(responses=[bytes.fromhex("50 03 00 19 01 F4")])
    client = UDSTransportClient(tr)
    resp = client.request(bytes.fromhex("10 03"))
    assert resp == bytes.fromhex("50 03 00 19 01 F4")


def test_transport_client_response_pending():
    tr = MockTransport(responses=[bytes.fromhex("7F 10 78"), bytes.fromhex("50 03 00 19 01 F4")])
    client = UDSTransportClient(tr, timing=UDSTiming(p2_ms=50, p2_star_ms=50, overall_timeout_ms=1000))
    resp = client.request(bytes.fromhex("10 03"))
    assert resp == bytes.fromhex("50 03 00 19 01 F4")
