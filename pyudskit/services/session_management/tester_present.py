from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex


class TesterPresent(UDSService):
    SID = 0x3E
    NAME = "TesterPresent"
    GROUP = "Session Management"

    def build_request(self, suppress_response: bool = True) -> ServiceResult:
        sub = 0x80 if suppress_response else 0x00
        data = bytes([self.SID, sub])
        return self._result(True, data, {"suppress_response": suppress_response}, "TesterPresent request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response SID", ["unexpected SID"])
        return self._result(True, data, {"subfunction": data[1] if len(data) > 1 else None}, "TesterPresent response")

    def validate(self, **kwargs) -> tuple[bool, list[str]]:
        return True, []
