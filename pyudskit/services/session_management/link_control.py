from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex


class LinkControl(UDSService):
    SID = 0x87
    NAME = "LinkControl"
    GROUP = "Session Management"

    SUBFUNCTIONS = {
        0x01: "verifyBaudrateTransitionWithFixedBaudrate",
        0x02: "verifyBaudrateTransitionWithSpecificBaudrate",
        0x03: "transitionBaudrate",
    }

    FIXED_BAUDRATES = {
        0x01: 9600,
        0x02: 19200,
        0x03: 38400,
        0x04: 57600,
        0x05: 115200,
        0x10: 250000,
        0x11: 500000,
        0x12: 1000000,
    }

    def build_request(self, subfunction: int, baudrate: int = 0x10, specific_baudrate: int | None = None) -> ServiceResult:
        ok, errors = self.validate(subfunction=subfunction)
        if not ok:
            return self._result(False, b"", {}, "Invalid subfunction", errors)
        payload = [self.SID, subfunction]
        if subfunction == 0x02 and specific_baudrate is not None:
            payload.extend(int(specific_baudrate).to_bytes(3, "big"))
        else:
            payload.append(baudrate & 0xFF)
        data = bytes(payload)
        return self._result(True, data, {"subfunction": subfunction}, "LinkControl request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response SID", ["unexpected SID"])
        return self._result(True, data, {"subfunction": data[1] if len(data) > 1 else None}, "LinkControl response")

    def validate(self, subfunction: int, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if subfunction not in self.SUBFUNCTIONS:
            errors.append("invalid subfunction")
        return (len(errors) == 0, errors)
