from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex


class RoutineControl(UDSService):
    SID = 0x31
    NAME = "RoutineControl"
    GROUP = "Routine Control"

    SUBFUNCTIONS = {"start": 0x01, "stop": 0x02, "result": 0x03}

    KNOWN_ROUTINES = {
        0xFF00: "EraseFlashMemory",
        0xFF01: "CheckFlashMemory",
        0xFF02: "CheckProgrammingDependencies",
        0x0202: "CheckProgrammingPreConditions",
        0x0203: "EraseMemory",
        0xF000: "VariantCoding",
    }

    def build_request(self, routine_id: int, action: str = "start", option_record: bytes = b"") -> ServiceResult:
        ok, errors = self.validate(routine_id=routine_id, action=action)
        if not ok:
            return self._result(False, b"", {}, "Invalid routine request", errors)
        sub = self.SUBFUNCTIONS[action]
        data = bytes([self.SID, sub, (routine_id >> 8) & 0xFF, routine_id & 0xFF]) + option_record
        return self._result(True, data, {"routine_id": routine_id, "action": action}, "RoutineControl request")

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
            fields["routine_id"] = (data[2] << 8) | data[3]
            fields["action"] = data[1]
            fields["result_hex"] = data[4:].hex().upper() if len(data) > 4 else ""
        return self._result(True, data, fields, "RoutineControl response")

    def validate(self, routine_id: int, action: str, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not (0 <= routine_id <= 0xFFFF):
            errors.append("routine_id must be 0..0xFFFF")
        if action not in self.SUBFUNCTIONS:
            errors.append("action must be start, stop, or result")
        return (len(errors) == 0, errors)
