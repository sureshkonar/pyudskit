from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex


class AccessTimingParameter(UDSService):
    SID = 0x83
    NAME = "AccessTimingParameter"
    GROUP = "Session Management"

    SUBFUNCTIONS = {
        0x01: "readExtendedTimingParameterSet",
        0x02: "setTimingParametersToDefaultValues",
        0x03: "readCurrentlyActiveTimingParameters",
        0x04: "setTimingParametersToGivenValues",
    }

    def build_request(self, subfunction: int, timing_params: bytes = b"") -> ServiceResult:
        ok, errors = self.validate(subfunction=subfunction)
        if not ok:
            return self._result(False, b"", {}, "Invalid subfunction", errors)
        data = bytes([self.SID, subfunction]) + timing_params
        return self._result(True, data, {"subfunction": subfunction}, "AccessTimingParameter request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response SID", ["unexpected SID"])
        return self._result(True, data, {"subfunction": data[1] if len(data) > 1 else None, "data_hex": parse_hex(response_hex)[2:].hex().upper()}, "AccessTimingParameter response")

    def validate(self, subfunction: int, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if subfunction not in self.SUBFUNCTIONS:
            errors.append("invalid subfunction")
        return (len(errors) == 0, errors)
