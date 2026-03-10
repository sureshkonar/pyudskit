from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex


class Authentication(UDSService):
    SID = 0x29
    NAME = "Authentication"
    GROUP = "Session Management"

    SUBFUNCTIONS = {
        0x00: "deAuthenticate",
        0x01: "verifyCertificateUnidirectional",
        0x02: "verifyCertificateBidirectional",
        0x03: "proofOfOwnership",
        0x04: "transmitCertificate",
        0x05: "requestChallengeForAuthentication",
        0x06: "verifyProofOfOwnershipUnidirectional",
        0x07: "verifyProofOfOwnershipBidirectional",
        0x08: "authenticationConfiguration",
    }

    def build_request(self, subfunction: int, data_hex: str = "") -> ServiceResult:
        ok, errors = self.validate(subfunction=subfunction)
        if not ok:
            return self._result(False, b"", {}, "Invalid subfunction", errors)
        data = bytes([self.SID, subfunction]) + parse_hex(data_hex)
        return self._result(True, data, {"subfunction": subfunction}, "Authentication request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response SID", ["unexpected SID"])
        return self._result(True, data, {"subfunction": data[1] if len(data) > 1 else None}, "Authentication response")

    def validate(self, subfunction: int, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if subfunction not in self.SUBFUNCTIONS:
            errors.append("invalid subfunction")
        return (len(errors) == 0, errors)
