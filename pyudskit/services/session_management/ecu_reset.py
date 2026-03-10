from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex


class ECUReset(UDSService):
    SID = 0x11
    NAME = "ECUReset"
    GROUP = "Session Management"

    RESET_TYPES = {
        "hard": 0x01,
        "keyOffOn": 0x02,
        "soft": 0x03,
    }

    def build_request(self, reset_type: str = "hard") -> ServiceResult:
        ok, errors = self.validate(reset_type=reset_type)
        if not ok:
            return self._result(False, b"", {}, "Invalid reset type", errors)
        sub = self.RESET_TYPES[reset_type]
        data = bytes([self.SID, sub])
        return self._result(True, data, {"reset_type": reset_type}, "ECUReset request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if len(data) < 2 or data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response SID", ["unexpected SID"])
        return self._result(True, data, {"reset_type": data[1]}, "ECUReset response")

    def validate(self, reset_type: str, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if reset_type not in self.RESET_TYPES:
            errors.append("reset_type must be hard, keyOffOn, or soft")
        return (len(errors) == 0, errors)
