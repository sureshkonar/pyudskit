from __future__ import annotations

from pyudskit.registry.dids import COMMON_DIDS
from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex, bytes_to_hex


class ReadScalingDataByIdentifier(UDSService):
    SID = 0x24
    NAME = "ReadScalingDataByIdentifier"
    GROUP = "Data Transmission"

    def build_request(self, did: int) -> ServiceResult:
        ok, errors = self.validate(did=did)
        if not ok:
            return self._result(False, b"", {}, "Invalid DID", errors)
        data = bytes([self.SID, (did >> 8) & 0xFF, did & 0xFF])
        return self._result(True, data, {"did": did}, "ReadScalingDataByIdentifier request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40) or len(data) < 3:
            return self._result(False, data, {}, "Unexpected response", ["unexpected response"])
        did = (data[1] << 8) | data[2]
        info = COMMON_DIDS.get(did, {})
        fields = {"did": did, "did_name": info.get("name"), "scaling_hex": bytes_to_hex(data[3:])}
        return self._result(True, data, fields, "ReadScalingDataByIdentifier response")

    def validate(self, did: int, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not (0 <= did <= 0xFFFF):
            errors.append("DID must be 0..0xFFFF")
        return (len(errors) == 0, errors)
