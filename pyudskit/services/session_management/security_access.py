from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex, bytes_to_hex


class SecurityAccess(UDSService):
    SID = 0x27
    NAME = "SecurityAccess"
    GROUP = "Session Management"

    def build_request_seed(self, level: int = 1) -> ServiceResult:
        ok, errors = self.validate(level=level)
        if not ok:
            return self._result(False, b"", {}, "Invalid security level", errors)
        sub = (level * 2) - 1
        data = bytes([self.SID, sub])
        return self._result(True, data, {"level": level, "type": "seed"}, "SecurityAccess seed request")

    def build_send_key(self, level: int, key_bytes: bytes) -> ServiceResult:
        ok, errors = self.validate(level=level)
        if not ok:
            return self._result(False, b"", {}, "Invalid security level", errors)
        sub = level * 2
        data = bytes([self.SID, sub]) + key_bytes
        return self._result(True, data, {"level": level, "type": "key"}, "SecurityAccess send key")

    def build_request(self, level: int = 1, key_bytes: bytes = b"") -> ServiceResult:
        if key_bytes:
            return self.build_send_key(level, key_bytes)
        return self.build_request_seed(level)

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response SID", ["unexpected SID"])
        if len(data) < 2:
            return self._result(False, data, {}, "Response too short", ["response too short"])
        sub = data[1]
        fields = {"subfunction": sub}
        if sub % 2 == 1 and len(data) > 2:
            fields["seed_hex"] = bytes_to_hex(data[2:])
        return self._result(True, data, fields, "SecurityAccess response")

    def parse_seed(self, response_hex: str) -> bytes:
        data = parse_hex(response_hex)
        if len(data) >= 3 and data[0] == (self.SID + 0x40):
            return data[2:]
        return b""

    def validate(self, level: int, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not isinstance(level, int) or not (1 <= level <= 7):
            errors.append("level must be 1..7")
        return (len(errors) == 0, errors)
