from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex


class ControlDTCSetting(UDSService):
    SID = 0x85
    NAME = "ControlDTCSetting"
    GROUP = "Session Management"

    SETTINGS = {"on": 0x01, "off": 0x02}

    def build_request(self, setting: str = "off", dtc_group: bytes = b"\xFF\xFF\xFF") -> ServiceResult:
        ok, errors = self.validate(setting=setting)
        if not ok:
            return self._result(False, b"", {}, "Invalid setting", errors)
        data = bytes([self.SID, self.SETTINGS[setting]]) + dtc_group
        return self._result(True, data, {"setting": setting}, "ControlDTCSetting request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response SID", ["unexpected SID"])
        return self._result(True, data, {"setting": data[1] if len(data) > 1 else None}, "ControlDTCSetting response")

    def validate(self, setting: str, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if setting not in self.SETTINGS:
            errors.append("setting must be on or off")
        return (len(errors) == 0, errors)
