from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex


class DiagnosticSessionControl(UDSService):
    SID = 0x10
    NAME = "DiagnosticSessionControl"
    GROUP = "Session Management"
    POSITIVE_RESPONSE_SID = 0x50

    SESSIONS = {
        "default": 0x01,
        "programming": 0x02,
        "extended": 0x03,
    }

    def build_request(self, session: str | int = "extended") -> ServiceResult:
        ok, errors = self.validate(session=session)
        if not ok:
            return self._result(False, b"", {}, "Invalid session", errors)
        sub = session if isinstance(session, int) else self.SESSIONS[session]
        data = bytes([self.SID, sub])
        return self._result(True, data, {"session": session}, "DiagnosticSessionControl request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        fields: dict = {}
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if not self.is_positive_response(data):
            return self._result(False, data, {}, "Unexpected response SID", ["unexpected SID"])
        if len(data) < 2:
            return self._result(False, data, {}, "Response too short", ["response too short"])
        session_byte = data[1]
        session_name = {
            0x01: "defaultDiagnosticSession",
            0x02: "programmingSession",
            0x03: "extendedDiagnosticSession",
        }.get(session_byte, f"0x{session_byte:02X}")
        fields["session"] = session_name
        if len(data) >= 4:
            fields["p2ServerMax_ms"] = int.from_bytes(data[2:4], "big")
        if len(data) >= 6:
            fields["p2StarServerMax_ms"] = int.from_bytes(data[4:6], "big")
        return self._result(True, data, fields, "DiagnosticSessionControl response")

    def validate(self, session: str | int, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if isinstance(session, int):
            if not (0 <= session <= 0xFF):
                errors.append("session subFunction must be 0..255")
        else:
            if session not in self.SESSIONS:
                errors.append("session must be one of: default, programming, extended")
        return (len(errors) == 0, errors)
