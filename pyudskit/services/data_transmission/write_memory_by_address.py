from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import build_alfid, parse_hex


class WriteMemoryByAddress(UDSService):
    SID = 0x3D
    NAME = "WriteMemoryByAddress"
    GROUP = "Data Transmission"

    def build_request(self, address: int, data: bytes, address_length: int = 4) -> ServiceResult:
        ok, errors = self.validate(address=address, data=data)
        if not ok:
            return self._result(False, b"", {}, "Invalid address/data", errors)
        alfid = build_alfid(address_length, 0)
        payload = bytes([self.SID, alfid]) + address.to_bytes(address_length, "big") + bytes(data)
        return self._result(True, payload, {"address": address}, "WriteMemoryByAddress request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response", ["unexpected response"])
        return self._result(True, data, {}, "WriteMemoryByAddress response")

    def validate(self, address: int, data: bytes, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if address < 0:
            errors.append("address must be >= 0")
        if not data:
            errors.append("data must not be empty")
        return (len(errors) == 0, errors)
