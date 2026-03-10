from __future__ import annotations

from pyudskit.registry.dids import COMMON_DIDS
from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex, bytes_to_hex


class ReadDataByIdentifier(UDSService):
    SID = 0x22
    NAME = "ReadDataByIdentifier"
    GROUP = "Data Transmission"
    POSITIVE_RESPONSE_SID = 0x62

    def build_request(self, dids: list[int]) -> ServiceResult:
        ok, errors = self.validate(dids=dids)
        if not ok:
            return self._result(False, b"", {}, "Invalid DIDs", errors)
        payload = [self.SID]
        for did in dids:
            payload.extend([(did >> 8) & 0xFF, did & 0xFF])
        data = bytes(payload)
        return self._result(True, data, {"dids": dids}, "ReadDataByIdentifier request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != self.POSITIVE_RESPONSE_SID or len(data) < 3:
            return self._result(False, data, {}, "Unexpected response", ["unexpected response"])
        did = (data[1] << 8) | data[2]
        info = COMMON_DIDS.get(did, {})
        fields = {
            "did": did,
            "did_name": info.get("name"),
            "data_hex": bytes_to_hex(data[3:]),
        }
        return self._result(True, data, fields, "ReadDataByIdentifier response")

    def validate(self, dids: list[int], **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not dids:
            errors.append("dids list must not be empty")
        for did in dids:
            if not (0 <= did <= 0xFFFF):
                errors.append(f"invalid DID: {did}")
        return (len(errors) == 0, errors)
