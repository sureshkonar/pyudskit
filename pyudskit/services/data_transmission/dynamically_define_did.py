from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex


class DynamicallyDefineDataIdentifier(UDSService):
    SID = 0x2C
    NAME = "DynamicallyDefineDataIdentifier"
    GROUP = "Data Transmission"

    SUBFUNCTIONS = {
        0x01: "defineByIdentifier",
        0x02: "defineByMemoryAddress",
        0x03: "clearDynamicallyDefinedDataIdentifier",
    }

    def build_define_by_identifier(self, dynamic_did: int, source_dids: list[tuple[int, int, int]]) -> ServiceResult:
        payload = [self.SID, 0x01, (dynamic_did >> 8) & 0xFF, dynamic_did & 0xFF]
        for source_did, position, size in source_dids:
            payload.extend([(source_did >> 8) & 0xFF, source_did & 0xFF, position & 0xFF, size & 0xFF])
        data = bytes(payload)
        return self._result(True, data, {"dynamic_did": dynamic_did}, "Define dynamic DID")

    def build_clear(self, dynamic_did: int) -> ServiceResult:
        data = bytes([self.SID, 0x03, (dynamic_did >> 8) & 0xFF, dynamic_did & 0xFF])
        return self._result(True, data, {"dynamic_did": dynamic_did}, "Clear dynamic DID")

    def build_request(self, subfunction: int, **kwargs) -> ServiceResult:
        ok, errors = self.validate(subfunction=subfunction, **kwargs)
        if not ok:
            return self._result(False, b"", {}, "Invalid dynamic DID request", errors)
        if subfunction == 0x01:
            return self.build_define_by_identifier(kwargs["dynamic_did"], kwargs["source_dids"])
        if subfunction == 0x03:
            return self.build_clear(kwargs["dynamic_did"])
        data = bytes([self.SID, subfunction])
        return self._result(True, data, {"subfunction": subfunction}, "Dynamic DID request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response", ["unexpected response"])
        fields = {"subfunction": data[1] if len(data) > 1 else None}
        if len(data) >= 4:
            fields["dynamic_did"] = (data[2] << 8) | data[3]
        return self._result(True, data, fields, "Dynamic DID response")

    def validate(self, subfunction: int, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if subfunction not in self.SUBFUNCTIONS:
            errors.append("invalid subfunction")
        if subfunction in (0x01, 0x03) and "dynamic_did" not in kwargs:
            errors.append("dynamic_did required")
        if subfunction == 0x01 and "source_dids" not in kwargs:
            errors.append("source_dids required")
        return (len(errors) == 0, errors)
