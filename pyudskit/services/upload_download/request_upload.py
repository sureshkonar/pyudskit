from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import build_alfid, parse_hex


class RequestUpload(UDSService):
    SID = 0x35
    NAME = "RequestUpload"
    GROUP = "Upload/Download"

    def build_request(self, address: int, size: int, address_length: int = 4, memory_size_length: int = 4) -> ServiceResult:
        ok, errors = self.validate(address=address, size=size)
        if not ok:
            return self._result(False, b"", {}, "Invalid request upload", errors)
        alfid = build_alfid(address_length, memory_size_length)
        payload = bytes([self.SID, 0x00, alfid])
        payload += address.to_bytes(address_length, "big")
        payload += size.to_bytes(memory_size_length, "big")
        return self._result(True, payload, {"address": address, "size": size}, "RequestUpload request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40) or len(data) < 2:
            return self._result(False, data, {}, "Unexpected response", ["unexpected response"])
        fields = {"length_format_identifier": data[1], "max_block_length_hex": data[2:].hex().upper()}
        return self._result(True, data, fields, "RequestUpload response")

    def validate(self, address: int, size: int, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if address < 0:
            errors.append("address must be >= 0")
        if size <= 0:
            errors.append("size must be > 0")
        return (len(errors) == 0, errors)
