from pyudskit import UDS


def test_security_algorithm_from_seed():
    uds = UDS()

    def xor_algo(seed: bytes, level: int) -> bytes:
        return bytes(b ^ 0xAA for b in seed)

    uds.register_security_algorithm("xor", xor_algo)
    req = uds.security_access_key_from_seed(1, "01 02 03 04", "xor")
    assert req["uds_bytes"].startswith("27 02")
