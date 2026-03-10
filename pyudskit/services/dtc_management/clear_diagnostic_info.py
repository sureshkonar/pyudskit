from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex


class ClearDiagnosticInformation(UDSService):
    SID = 0x14
    NAME = "ClearDiagnosticInformation"
    GROUP = "DTC Management"

    DTC_GROUPS = {
        "all": 0xFFFFFF,
        "powertrain": 0x000000,
        "chassis": 0x400000,
        "body": 0x800000,
        "network": 0xC00000,
    }

    def build_request(self, group: str | int = "all") -> ServiceResult:
        ok, errors = self.validate(group=group)
        if not ok:
            return self._result(False, b"", {}, "Invalid DTC group", errors)
        if isinstance(group, str):
            value = self.DTC_GROUPS[group]
        else:
            value = int(group)
        group_bytes = value.to_bytes(3, "big")
        data = bytes([self.SID]) + group_bytes
        return self._result(True, data, {"group": group}, "ClearDiagnosticInformation request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response", ["unexpected response"])
        return self._result(True, data, {}, "ClearDiagnosticInformation response")

    def validate(self, group, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if isinstance(group, str):
            if group not in self.DTC_GROUPS:
                errors.append("invalid DTC group")
        elif not (0 <= int(group) <= 0xFFFFFF):
            errors.append("group must be 0..0xFFFFFF")
        return (len(errors) == 0, errors)
