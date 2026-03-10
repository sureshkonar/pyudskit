from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex


class ReadDataByPeriodicIdentifier(UDSService):
    SID = 0x2A
    NAME = "ReadDataByPeriodicIdentifier"
    GROUP = "Data Transmission"

    RATES = {
        "slow": 0x01,
        "medium": 0x02,
        "fast": 0x03,
        "stop": 0x04,
    }

    def build_request(self, rate: str, periodic_dids: list[int]) -> ServiceResult:
        ok, errors = self.validate(rate=rate, periodic_dids=periodic_dids)
        if not ok:
            return self._result(False, b"", {}, "Invalid periodic request", errors)
        payload = [self.SID, self.RATES[rate]]
        for did in periodic_dids:
            payload.append(did & 0xFF)
        data = bytes(payload)
        return self._result(True, data, {"rate": rate, "periodic_dids": periodic_dids}, "ReadDataByPeriodicIdentifier request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response", ["unexpected response"])
        return self._result(True, data, {"rate": data[1] if len(data) > 1 else None}, "ReadDataByPeriodicIdentifier response")

    def validate(self, rate: str, periodic_dids: list[int], **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if rate not in self.RATES:
            errors.append("rate must be slow, medium, fast, or stop")
        if not periodic_dids:
            errors.append("periodic_dids must not be empty")
        for did in periodic_dids:
            if not (0 <= did <= 0xFF):
                errors.append("periodic DID must be 1 byte")
        return (len(errors) == 0, errors)
