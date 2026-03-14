from __future__ import annotations

from typing import Optional

from pyudskit.transport.base import Transport, TransportConfig
from pyudskit.transport.isotp import IsoTpReassembler, IsoTpSegmenter


class CANTransport(Transport):
    """CAN transport using python-can. Requires python-can installed."""

    def __init__(self, channel: str, bustype: str, rx_id: int, tx_id: int, config: Optional[TransportConfig] = None) -> None:
        super().__init__(config=config)
        try:
            import can  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("python-can is required for CANTransport") from exc
        self._can = can
        self.bus = can.Bus(channel=channel, bustype=bustype)
        self.rx_id = rx_id
        self.tx_id = tx_id
        self._reassembler = IsoTpReassembler()
        self._segmenter = IsoTpSegmenter()

    def send(self, request_bytes: bytes) -> None:
        for frame in self._segmenter.segment(request_bytes):
            msg = self._can.Message(arbitration_id=self.tx_id, data=frame, is_extended_id=False)
            self.bus.send(msg)

    def recv(self, timeout_ms: Optional[int] = None) -> Optional[bytes]:
        timeout = (timeout_ms or self.config.timeout_ms) / 1000.0
        msg = self.bus.recv(timeout=timeout)
        if msg is None:
            return None
        payload = self._reassembler.feed(bytes(msg.data))
        return payload

    def close(self) -> None:
        try:
            self.bus.shutdown()
        except Exception:
            pass
