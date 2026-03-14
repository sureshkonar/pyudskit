from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class IsoTpConfig:
    stmin_ms: int = 0
    block_size: int = 0
    wft_max: int = 0


class IsoTpError(RuntimeError):
    pass


class IsoTpReassembler:
    """Minimal ISO-TP reassembler for incoming frames."""

    def __init__(self) -> None:
        self._buf = bytearray()
        self._expected_len: Optional[int] = None
        self._next_seq: int = 1

    def feed(self, frame: bytes) -> Optional[bytes]:
        if not frame:
            return None
        pci = frame[0]
        frame_type = (pci & 0xF0) >> 4
        if frame_type == 0x0:  # Single Frame
            length = pci & 0x0F
            return bytes(frame[1 : 1 + length])
        if frame_type == 0x1:  # First Frame
            length = ((pci & 0x0F) << 8) | frame[1]
            self._expected_len = length
            self._buf = bytearray(frame[2:])
            self._next_seq = 1
            return self._maybe_complete()
        if frame_type == 0x2:  # Consecutive Frame
            seq = pci & 0x0F
            if seq != (self._next_seq & 0x0F):
                raise IsoTpError("sequence mismatch")
            self._next_seq += 1
            self._buf.extend(frame[1:])
            return self._maybe_complete()
        if frame_type == 0x3:  # Flow Control (ignored by reassembler)
            return None
        raise IsoTpError("unknown PCI")

    def _maybe_complete(self) -> Optional[bytes]:
        if self._expected_len is None:
            return None
        if len(self._buf) >= self._expected_len:
            payload = bytes(self._buf[: self._expected_len])
            self._reset()
            return payload
        return None

    def _reset(self) -> None:
        self._buf = bytearray()
        self._expected_len = None
        self._next_seq = 1


class IsoTpSegmenter:
    """Segment outgoing payloads into ISO-TP frames (8-byte CAN)."""

    def segment(self, payload: bytes) -> list[bytes]:
        if len(payload) <= 7:
            return [bytes([len(payload) & 0x0F]) + payload.ljust(7, b"\x00")]
        frames: list[bytes] = []
        length = len(payload)
        first = bytes([0x10 | ((length >> 8) & 0x0F), length & 0xFF]) + payload[:6]
        frames.append(first.ljust(8, b"\x00"))
        seq = 1
        idx = 6
        while idx < length:
            chunk = payload[idx : idx + 7]
            frame = bytes([0x20 | (seq & 0x0F)]) + chunk
            frames.append(frame.ljust(8, b"\x00"))
            seq = (seq + 1) & 0x0F
            idx += 7
        return frames
