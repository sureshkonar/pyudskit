from __future__ import annotations

from collections import deque
from typing import Callable, Deque, Optional

from pyudskit.transport.base import Transport, TransportConfig


class MockTransport(Transport):
    """Mock transport for tests and offline simulations."""

    def __init__(
        self,
        responses: Optional[list[bytes]] = None,
        handler: Optional[Callable[[bytes], Optional[bytes]]] = None,
        config: Optional[TransportConfig] = None,
    ) -> None:
        super().__init__(config=config)
        self.sent: list[bytes] = []
        self._queue: Deque[bytes] = deque(responses or [])
        self._handler = handler

    def send(self, request_bytes: bytes) -> None:
        self.sent.append(request_bytes)
        if self._handler:
            resp = self._handler(request_bytes)
            if resp:
                self._queue.append(resp)

    def recv(self, timeout_ms: Optional[int] = None) -> Optional[bytes]:
        if self._queue:
            return self._queue.popleft()
        return None

    def close(self) -> None:
        self._queue.clear()
