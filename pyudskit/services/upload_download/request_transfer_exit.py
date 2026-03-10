from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex


class RequestTransferExit(UDSService):
    SID = 0x37
    NAME = "RequestTransferExit"
    GROUP = "Upload/Download"

    def build_request(self, transfer_response_parameter: bytes = b"") -> ServiceResult:
        data = bytes([self.SID]) + transfer_response_parameter
        return self._result(True, data, {}, "RequestTransferExit request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response", ["unexpected response"])
        return self._result(True, data, {"data_hex": data[1:].hex().upper()}, "RequestTransferExit response")

    def validate(self, **kwargs) -> tuple[bool, list[str]]:
        return True, []
