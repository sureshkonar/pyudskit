from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex


class InputOutputControlByIdentifier(UDSService):
    SID = 0x2F
    NAME = "InputOutputControlByIdentifier"
    GROUP = "I/O Control"

    CONTROL_OPTIONS = {
        "returnControlToECU": 0x00,
        "resetToDefault": 0x01,
        "freezeCurrentState": 0x02,
        "shortTermAdjustment": 0x03,
    }

    def build_request(
        self,
        did: int,
        control_option: str,
        control_enable_mask: bytes = b"",
        control_value: bytes = b"",
    ) -> ServiceResult:
        ok, errors = self.validate(did=did, control_option=control_option)
        if not ok:
            return self._result(False, b"", {}, "Invalid I/O control request", errors)
        payload = [self.SID, (did >> 8) & 0xFF, did & 0xFF, self.CONTROL_OPTIONS[control_option]]
        data = bytes(payload) + control_enable_mask + control_value
        return self._result(True, data, {"did": did, "control_option": control_option}, "InputOutputControl request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response", ["unexpected response"])
        fields = {}
        if len(data) >= 4:
            fields["did"] = (data[1] << 8) | data[2]
            fields["control_option"] = data[3]
        return self._result(True, data, fields, "InputOutputControl response")

    def validate(self, did: int, control_option: str, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not (0 <= did <= 0xFFFF):
            errors.append("DID must be 0..0xFFFF")
        if control_option not in self.CONTROL_OPTIONS:
            errors.append("invalid control_option")
        return (len(errors) == 0, errors)
