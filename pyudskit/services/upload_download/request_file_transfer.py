from __future__ import annotations

from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.utils import parse_hex


class RequestFileTransfer(UDSService):
    SID = 0x38
    NAME = "RequestFileTransfer"
    GROUP = "Upload/Download"

    MODE_OF_OPERATION = {
        0x01: "addFile",
        0x02: "deleteFile",
        0x03: "replaceFile",
        0x04: "readFile",
        0x05: "readDir",
    }

    def build_request(
        self,
        mode: int,
        file_path: str,
        compression_method: int = 0x00,
        encrypting_method: int = 0x00,
        file_size: int = 0,
    ) -> ServiceResult:
        ok, errors = self.validate(mode=mode, file_path=file_path)
        if not ok:
            return self._result(False, b"", {}, "Invalid file transfer", errors)
        dfi = ((compression_method & 0x0F) << 4) | (encrypting_method & 0x0F)
        path_bytes = file_path.encode("ascii", errors="ignore")
        payload = bytes([self.SID, mode, dfi, len(path_bytes)]) + path_bytes
        if file_size:
            payload += int(file_size).to_bytes(4, "big")
        return self._result(True, payload, {"mode": mode, "file_path": file_path}, "RequestFileTransfer request")

    def parse_response(self, response_hex: str) -> ServiceResult:
        data = parse_hex(response_hex)
        if not data:
            return self._result(False, b"", {}, "Empty response", ["empty response"])
        if self.is_negative_response(data):
            return self._result(False, data, {}, "Negative response", ["negative response"])
        if data[0] != (self.SID + 0x40):
            return self._result(False, data, {}, "Unexpected response", ["unexpected response"])
        fields = {"mode": data[1] if len(data) > 1 else None, "data_hex": data[2:].hex().upper()}
        return self._result(True, data, fields, "RequestFileTransfer response")

    def validate(self, mode: int, file_path: str, **kwargs) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if mode not in self.MODE_OF_OPERATION:
            errors.append("invalid mode")
        if not file_path:
            errors.append("file_path required")
        return (len(errors) == 0, errors)
