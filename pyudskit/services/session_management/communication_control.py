from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex


class CommunicationControl(UDSService):
    SID = 0x28
    NAME = "CommunicationControl"
    GROUP = "Session Management"

    CONTROL_TYPES = {
        "enableRxAndTx": 0x00,
        "enableRxAndDisableTx": 0x01,
        "disableRxAndEnableTx": 0x02,
        "disableRxAndTx": 0x03,
    }

    COMM_TYPES = {
        "normalCommunication": 0x01,
        "nmCommunication": 0x02,
        "networkManagement": 0x03,
    }

    def build_request(self, control_type: str = "disableRxAndTx", comm_type: str = "normalCommunication") -> ServiceResult:
        ok, errors = self.validate(control_type=control_type, comm_type=comm_type)
        if not ok:
            return self._result(False, b"", {}, "Invalid communication control", errors)
        data = bytes([self.SID, self.CONTROL_TYPES[control_type], self.COMM_TYPES[comm_type]])
        return self._result(True, data, {"control_type": control_type, "comm_type": comm_type}, "CommunicationControl request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response SID", ["unexpected SID"])
        return self._result(True, data, {"control_type": data[1] if len(data) > 1 else None}, "CommunicationControl response")

    def validate(self, control_type: str, comm_type: str = "normalCommunication", **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if control_type not in self.CONTROL_TYPES:
            errors.append("invalid control_type")
        if comm_type not in self.COMM_TYPES:
            errors.append("invalid comm_type")
        return (len(errors) == 0, errors)
