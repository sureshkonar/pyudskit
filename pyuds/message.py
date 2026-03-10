from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from pyuds.registry.nrc import UDS_NRC
from pyuds.registry.services import UDS_SERVICES
from pyuds.registry.dtc_status import DTC_STATUS_BITS
from pyuds.utils import bytes_to_hex, parse_hex


@dataclass
class UDSMessage:
    """Parsed and validated representation of a single UDS Protocol Data Unit (PDU)."""

    raw_bytes: bytes

    @classmethod
    def from_hex(cls, hex_str: str) -> "UDSMessage":
        """Parse from hex string. Accepts spaces, no-spaces, 0x prefix."""
        return cls(parse_hex(hex_str))

    @classmethod
    def from_bytes(cls, data: bytes) -> "UDSMessage":
        """Parse from raw bytes."""
        if not isinstance(data, (bytes, bytearray)):
            raise ValueError("data must be bytes")
        return cls(bytes(data))

    @property
    def service_id(self) -> int:
        """First byte — the Service Identifier (SID)."""
        if not self.raw_bytes:
            return 0
        return self.raw_bytes[0]

    @property
    def is_positive_response(self) -> bool:
        """True if SID is in range 0x40–0xFF (SID + 0x40 convention)."""
        sid = self.service_id
        return 0x40 <= sid <= 0xFF and sid != 0x7F

    @property
    def is_negative_response(self) -> bool:
        """True if SID == 0x7F."""
        return self.service_id == 0x7F

    @property
    def is_request(self) -> bool:
        """True if this is a client request frame."""
        return not self.is_positive_response and not self.is_negative_response

    @property
    def request_service_id(self) -> int:
        """For positive responses, returns SID - 0x40. For NRC, returns byte[1]."""
        if self.is_positive_response:
            return self.service_id - 0x40
        if self.is_negative_response and len(self.raw_bytes) > 1:
            return self.raw_bytes[1]
        return self.service_id

    @property
    def nrc(self) -> Optional[int]:
        """Negative Response Code byte (byte[2]) for 0x7F frames."""
        if self.is_negative_response and len(self.raw_bytes) > 2:
            return self.raw_bytes[2]
        return None

    @property
    def nrc_name(self) -> Optional[str]:
        """Human-readable NRC name from registry."""
        code = self.nrc
        if code is None:
            return None
        return UDS_NRC.get(code)

    @property
    def service_info(self) -> dict:
        """Full service entry from UDS_SERVICES registry."""
        return UDS_SERVICES.get(self.request_service_id, {})

    @property
    def service_name(self) -> str:
        """Human-readable service name with response type tag."""
        name = self.service_info.get("name", "UnknownService")
        if self.is_positive_response:
            return f"{name} [Positive Response]"
        if self.is_negative_response:
            return f"{name} [Negative Response]"
        return f"{name} [Request]"

    def to_hex(self, sep: str = " ") -> str:
        """Return hex string representation."""
        return bytes_to_hex(self.raw_bytes, sep=sep)

    def decode_dtc_status(self, status_byte: int) -> list[str]:
        """Return list of active DTC status flag names for a status byte."""
        return [name for bit, name in DTC_STATUS_BITS.items() if status_byte & bit]

    def validate(self) -> tuple[bool, str]:
        """Validate message structure. Returns (is_valid, error_message)."""
        if not self.raw_bytes:
            return False, "empty PDU"
        if self.is_negative_response:
            if len(self.raw_bytes) < 3:
                return False, "negative response too short"
            return True, "ok"
        svc = UDS_SERVICES.get(self.request_service_id)
        if svc:
            min_len = svc.get("min_length", 1)
            max_len = svc.get("max_length", 0)
            if len(self.raw_bytes) < min_len:
                return False, "message too short"
            if max_len and len(self.raw_bytes) > max_len:
                return False, "message too long"
        return True, "ok"

    def __repr__(self) -> str:
        return f"UDSMessage('{self.service_name}' | {self.to_hex()})"
