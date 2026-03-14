from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class TransportConfig:
    timeout_ms: int = 2000


class Transport(ABC):
    """Abstract transport interface for UDS over CAN/DoIP/etc."""

    def __init__(self, config: Optional[TransportConfig] = None) -> None:
        self.config = config or TransportConfig()

    @abstractmethod
    def send(self, request_bytes: bytes) -> None:
        """Send raw UDS payload bytes."""
        ...

    @abstractmethod
    def recv(self, timeout_ms: Optional[int] = None) -> Optional[bytes]:
        """Receive raw UDS payload bytes, or None on timeout."""
        ...

    @abstractmethod
    def close(self) -> None:
        """Close underlying transport resources."""
        ...
