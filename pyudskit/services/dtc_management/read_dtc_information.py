from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex, bytes_to_hex, split_dtc
from pyudskit.registry.dtc_status import DTC_STATUS_BITS


class ReadDTCInformation(UDSService):
    SID = 0x19
    NAME = "ReadDTCInformation"
    GROUP = "DTC Management"

    SUBFUNCTIONS = {
        0x01: "reportNumberOfDTCByStatusMask",
        0x02: "reportDTCByStatusMask",
        0x03: "reportDTCSnapshotIdentification",
        0x04: "reportDTCSnapshotRecordByDTCNumber",
        0x05: "reportDTCSnapshotRecordByRecordNumber",
        0x06: "reportDTCExtendedDataRecordByDTCNumber",
        0x07: "reportNumberOfDTCBySeverityMaskRecord",
        0x08: "reportDTCBySeverityMaskRecord",
        0x09: "reportSeverityInformationOfDTC",
        0x0A: "reportSupportedDTC",
        0x0B: "reportFirstTestFailedDTC",
        0x0C: "reportFirstConfirmedDTC",
        0x0D: "reportMostRecentTestFailedDTC",
        0x0E: "reportMostRecentConfirmedDTC",
        0x0F: "reportMirrorMemoryDTCByStatusMask",
        0x10: "reportMirrorMemoryDTCExtendedDataRecordByDTCNumber",
        0x11: "reportNumberOfMirrorMemoryDTCByStatusMask",
        0x12: "reportNumberOfEmissionsOBDDTCByStatusMask",
        0x13: "reportEmissionsOBDDTCByStatusMask",
        0x14: "reportDTCFaultDetectionCounter",
        0x15: "reportDTCWithPermanentStatus",
    }

    def build_request_by_status_mask(self, status_mask: int = 0x08) -> ServiceResult:
        return self.build_request(0x02, status_mask=status_mask)

    def build_request_number_by_status(self, status_mask: int = 0x08) -> ServiceResult:
        return self.build_request(0x01, status_mask=status_mask)

    def build_request_snapshot_id(self) -> ServiceResult:
        return self.build_request(0x03)

    def build_request_snapshot_by_dtc(self, dtc: int, record_num: int = 0xFF) -> ServiceResult:
        return self.build_request(0x04, dtc=dtc, record_num=record_num)

    def build_request_snapshot_by_record(self, record_num: int) -> ServiceResult:
        return self.build_request(0x05, record_num=record_num)

    def build_request_extended_by_dtc(self, dtc: int, record_num: int = 0xFF) -> ServiceResult:
        return self.build_request(0x06, dtc=dtc, record_num=record_num)

    def build_request_by_severity(self, severity_mask: int, status_mask: int) -> ServiceResult:
        return self.build_request(0x08, severity_mask=severity_mask, status_mask=status_mask)

    def build_request_supported_dtcs(self) -> ServiceResult:
        return self.build_request(0x0A)

    def build_request_first_failed(self) -> ServiceResult:
        return self.build_request(0x0B)

    def build_request_first_confirmed(self) -> ServiceResult:
        return self.build_request(0x0C)

    def build_request_most_recent_failed(self) -> ServiceResult:
        return self.build_request(0x0D)

    def build_request_most_recent_confirmed(self) -> ServiceResult:
        return self.build_request(0x0E)

    def build_request_fault_counter(self) -> ServiceResult:
        return self.build_request(0x14)

    def build_request_permanent(self) -> ServiceResult:
        return self.build_request(0x15)

    def build_request(self, subfunction: int, **kwargs) -> ServiceResult:
        ok, errors = self.validate(subfunction=subfunction)
        if not ok:
            return self._result(False, b"", {}, "Invalid subfunction", errors)
        payload = [self.SID, subfunction]
        if subfunction in (0x01, 0x02):
            payload.append(kwargs.get("status_mask", 0x08) & 0xFF)
        elif subfunction in (0x04, 0x06):
            dtc = int(kwargs.get("dtc", 0))
            payload.extend(dtc.to_bytes(3, "big"))
            payload.append(kwargs.get("record_num", 0xFF) & 0xFF)
        elif subfunction == 0x05:
            payload.append(kwargs.get("record_num", 0xFF) & 0xFF)
        elif subfunction == 0x08:
            payload.append(kwargs.get("severity_mask", 0) & 0xFF)
            payload.append(kwargs.get("status_mask", 0) & 0xFF)
        data = bytes(payload)
        return self._result(True, data, {"subfunction": subfunction}, "ReadDTCInformation request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40) or len(data) < 2:
            return self._result(False, data, {}, "Unexpected response", ["unexpected response"])
        subfunction = data[1]
        fields: dict = {"subfunction": subfunction}
        payload = data[2:]
        if subfunction == 0x02 and payload:
            fields["dtcs"] = self.parse_dtc_list(payload)
        else:
            fields["data_hex"] = bytes_to_hex(payload)
        return self._result(True, data, fields, "ReadDTCInformation response")

    def parse_dtc_list(self, data: bytes) -> list[dict]:
        results: list[dict] = []
        i = 0
        while i + 3 < len(data):
            dtc_bytes = data[i : i + 3]
            status = data[i + 3]
            _, code = split_dtc(dtc_bytes)
            flags = [name for bit, name in DTC_STATUS_BITS.items() if status & bit]
            results.append({"dtc": code, "status_byte": status, "status_flags": flags})
            i += 4
        return results

    def validate(self, subfunction: int, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if subfunction not in self.SUBFUNCTIONS:
            errors.append("invalid subfunction")
        return (len(errors) == 0, errors)
