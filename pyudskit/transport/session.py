from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional

from pyudskit.message import UDSMessage
from pyudskit.transport.base import Transport


@dataclass
class UDSTiming:
    p2_ms: int = 50
    p2_star_ms: int = 5000
    overall_timeout_ms: int = 10000


class UDSTransportClient:
    """End-to-end UDS request/response over a Transport."""

    def __init__(self, transport: Transport, timing: Optional[UDSTiming] = None) -> None:
        self.transport = transport
        self.timing = timing or UDSTiming()

    def request(self, request_bytes: bytes, timeout_ms: Optional[int] = None) -> Optional[bytes]:
        self.transport.send(request_bytes)
        deadline = time.time() + ((timeout_ms or self.timing.overall_timeout_ms) / 1000.0)
        wait_ms = self.timing.p2_ms

        while True:
            remaining = deadline - time.time()
            if remaining <= 0:
                return None
            resp = self.transport.recv(int(min(wait_ms, remaining * 1000)))
            if resp is None:
                continue
            msg = UDSMessage.from_bytes(resp)
            if msg.is_negative_response and msg.nrc == 0x78:
                wait_ms = self.timing.p2_star_ms
                continue
            return resp

    def request_message(self, request_bytes: bytes, timeout_ms: Optional[int] = None) -> Optional[UDSMessage]:
        resp = self.request(request_bytes, timeout_ms=timeout_ms)
        if resp is None:
            return None
        return UDSMessage.from_bytes(resp)
