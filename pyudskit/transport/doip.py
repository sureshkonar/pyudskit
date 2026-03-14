from __future__ import annotations

from typing import Optional

from pyudskit.transport.base import Transport, TransportConfig


class DoIPTransport(Transport):
    """DoIP transport using doipy. Requires doipy installed."""

    def __init__(self, ip: str, logical_address: int, tx_id: int, rx_id: int, config: Optional[TransportConfig] = None) -> None:
        super().__init__(config=config)
        try:
            from doipy import DoIPClient  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("doipy is required for DoIPTransport") from exc
        self.client = DoIPClient(ip, logical_address)
        self.tx_id = tx_id
        self.rx_id = rx_id

    def send(self, request_bytes: bytes) -> None:
        self.client.send_diagnostic_message(self.tx_id, request_bytes)

    def recv(self, timeout_ms: Optional[int] = None) -> Optional[bytes]:
        timeout = (timeout_ms or self.config.timeout_ms) / 1000.0
        msg = self.client.receive_diagnostic_message(timeout)
        if msg is None:
            return None
        return msg.payload

    def close(self) -> None:
        try:
            self.client.close()
        except Exception:
            pass
