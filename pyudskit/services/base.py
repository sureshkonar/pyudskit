from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from pyudskit.message import UDSMessage
from pyudskit.utils import bytes_to_hex


@dataclass
class ServiceResult:
    """
    Returned by every service's build_request() and parse_response().
    """

    success: bool
    uds_message: Optional[UDSMessage]
    hex_bytes: str
    fields: dict
    description: str
    errors: list[str] = field(default_factory=list)

    def __repr__(self) -> str:
        status = "OK" if self.success else "ERROR"
        return f"ServiceResult({status} | {self.hex_bytes} | {self.description})"


class UDSService(ABC):
    """
    Abstract base class for all ISO 14229 UDS services.
    """

    SID: int = 0x00
    NAME: str = "UDSService"
    GROUP: str = "Unknown"
    POSITIVE_RESPONSE_SID: int = 0x00

    @abstractmethod
    def build_request(self, **kwargs) -> ServiceResult:
        """Build the request PDU bytes for this service."""
        ...

    @abstractmethod
    def parse_response(self, response_hex: str) -> ServiceResult:
        """Parse a raw response PDU into structured fields."""
        ...

    @abstractmethod
    def validate(self, **kwargs) -> tuple[bool, list[str]]:
        """
        Validate input parameters before building.
        Returns (is_valid, list_of_error_messages).
        """
        ...

    def get_expected_response_sid(self) -> int:
        return self.SID + 0x40

    def is_positive_response(self, response_bytes: bytes) -> bool:
        return len(response_bytes) > 0 and response_bytes[0] == self.get_expected_response_sid()

    def is_negative_response(self, response_bytes: bytes) -> bool:
        return len(response_bytes) > 0 and response_bytes[0] == 0x7F

    def describe(self) -> dict:
        return {
            "sid": f"0x{self.SID:02X}",
            "name": self.NAME,
            "group": self.GROUP,
            "positive_response_sid": f"0x{self.get_expected_response_sid():02X}",
        }

    def _result(self, success: bool, data: bytes, fields: dict, description: str, errors: list[str] | None = None) -> ServiceResult:
        return ServiceResult(
            success=success,
            uds_message=UDSMessage.from_bytes(data) if data is not None else None,
            hex_bytes=bytes_to_hex(data) if data is not None else "",
            fields=fields,
            description=description,
            errors=errors or [],
        )
