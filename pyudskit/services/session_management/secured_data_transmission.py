from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex


class SecuredDataTransmission(UDSService):
    SID = 0x84
    NAME = "SecuredDataTransmission"
    GROUP = "Session Management"

    def build_request(self, data_hex: str = "") -> ServiceResult:
        data = bytes([self.SID]) + parse_hex(data_hex)
        return self._result(True, data, {"data_hex": data_hex}, "SecuredDataTransmission request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response SID", ["unexpected SID"])
        return self._result(True, data, {"data_hex": data[1:].hex().upper()}, "SecuredDataTransmission response")

    def validate(self, **kwargs) -> tuple[bool, list[str]]:
        return True, []
