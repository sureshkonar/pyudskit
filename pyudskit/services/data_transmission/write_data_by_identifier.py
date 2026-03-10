from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex


class WriteDataByIdentifier(UDSService):
    SID = 0x2E
    NAME = "WriteDataByIdentifier"
    GROUP = "Data Transmission"

    def build_request(self, did: int, data: bytes | str) -> ServiceResult:
        ok, errors = self.validate(did=did, data=data)
        if not ok:
            return self._result(False, b"", {}, "Invalid DID/data", errors)
        data_bytes = data if isinstance(data, (bytes, bytearray)) else parse_hex(str(data))
        payload = bytes([self.SID, (did >> 8) & 0xFF, did & 0xFF]) + bytes(data_bytes)
        return self._result(True, payload, {"did": did}, "WriteDataByIdentifier request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response", ["unexpected response"])
        return self._result(True, data, {"did": (data[1] << 8) | data[2] if len(data) >= 3 else None}, "WriteDataByIdentifier response")

    def validate(self, did: int, data, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not (0 <= did <= 0xFFFF):
            errors.append("DID must be 0..0xFFFF")
        if data is None:
            errors.append("data must not be None")
        return (len(errors) == 0, errors)
