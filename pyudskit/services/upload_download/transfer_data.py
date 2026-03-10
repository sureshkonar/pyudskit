from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex


class TransferData(UDSService):
    SID = 0x36
    NAME = "TransferData"
    GROUP = "Upload/Download"

    def build_request(self, block_sequence_counter: int, data: bytes | str) -> ServiceResult:
        ok, errors = self.validate(block_sequence_counter=block_sequence_counter, data=data)
        if not ok:
            return self._result(False, b"", {}, "Invalid transfer data", errors)
        data_bytes = data if isinstance(data, (bytes, bytearray)) else parse_hex(str(data))
        payload = bytes([self.SID, block_sequence_counter & 0xFF]) + bytes(data_bytes)
        return self._result(True, payload, {"block_sequence_counter": block_sequence_counter}, "TransferData request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response", ["unexpected response"])
        return self._result(True, data, {"block_sequence_counter": data[1] if len(data) > 1 else None}, "TransferData response")

    def validate(self, block_sequence_counter: int, data, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not (0 <= block_sequence_counter <= 0xFF):
            errors.append("block_sequence_counter must be 0..255")
        if data is None:
            errors.append("data must not be None")
        return (len(errors) == 0, errors)
