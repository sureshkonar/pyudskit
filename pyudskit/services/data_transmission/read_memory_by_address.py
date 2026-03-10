from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex, build_alfid, bytes_to_hex


class ReadMemoryByAddress(UDSService):
    SID = 0x23
    NAME = "ReadMemoryByAddress"
    GROUP = "Data Transmission"

    def build_request(self, address: int, length: int, address_length: int = 4, memory_size_length: int = 1) -> ServiceResult:
        ok, errors = self.validate(address=address, length=length)
        if not ok:
            return self._result(False, b"", {}, "Invalid address/length", errors)
        alfid = build_alfid(address_length, memory_size_length)
        data = bytes([self.SID, alfid]) + address.to_bytes(address_length, "big") + length.to_bytes(memory_size_length, "big")
        return self._result(True, data, {"address": address, "length": length}, "ReadMemoryByAddress request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response", ["unexpected response"])
        return self._result(True, data, {"data_hex": bytes_to_hex(data[1:])}, "ReadMemoryByAddress response")

    def validate(self, address: int, length: int, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if address < 0:
            errors.append("address must be >= 0")
        if length <= 0:
            errors.append("length must be > 0")
        return (len(errors) == 0, errors)
