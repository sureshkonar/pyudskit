from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex


class ResponseOnEvent(UDSService):
    SID = 0x86
    NAME = "ResponseOnEvent"
    GROUP = "Session Management"

    EVENT_TYPES = {
        0x00: "stopResponseOnEvent",
        0x01: "onDTCStatusChange",
        0x02: "onTimerInterrupt",
        0x03: "onChangeOfDataIdentifier",
        0x04: "reportActivatedEvents",
        0x05: "startResponseOnEvent",
        0x06: "clearResponseOnEvent",
        0x07: "onComparisonOfValues",
    }

    def build_request(
        self,
        event_type: int,
        event_window: int = 0x02,
        event_type_record: bytes = b"",
        service_to_respond: bytes = b"",
    ) -> ServiceResult:
        ok, errors = self.validate(event_type=event_type)
        if not ok:
            return self._result(False, b"", {}, "Invalid event_type", errors)
        data = bytes([self.SID, event_type, event_window]) + event_type_record + service_to_respond
        return self._result(True, data, {"event_type": event_type}, "ResponseOnEvent request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response SID", ["unexpected SID"])
        return self._result(True, data, {"event_type": data[1] if len(data) > 1 else None}, "ResponseOnEvent response")

    def validate(self, event_type: int, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if event_type not in self.EVENT_TYPES:
            errors.append("invalid event_type")
        return (len(errors) == 0, errors)
