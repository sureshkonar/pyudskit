from pyuds import UDS

uds = UDS()

print(uds.encode_request("Switch to extended diagnostic session"))
print(uds.decode_response("7F 22 31"))
print(uds.read_did(0xF190))
print(uds.read_dtcs())
