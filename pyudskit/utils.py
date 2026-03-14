import json
import re
from typing import Any

from pyudskit.registry.services import UDS_SERVICES
from pyudskit.registry.dtc_status import DTC_STATUS_BITS


HEX_RE = re.compile(r"^[0-9A-Fa-f]+$")


def parse_hex(hex_str: str) -> bytes:
    """Accept hex with/without spaces and 0x prefix. Raise ValueError on bad input."""
    if not isinstance(hex_str, str):
        raise ValueError("hex_str must be a string")
    cleaned = hex_str.strip().replace(" ", "")
    if cleaned.startswith("0x") or cleaned.startswith("0X"):
        cleaned = cleaned[2:]
    if cleaned == "":
        return b""
    if len(cleaned) % 2 != 0:
        raise ValueError("hex_str must have even length")
    if not HEX_RE.match(cleaned):
        raise ValueError("hex_str contains non-hex characters")
    return bytes.fromhex(cleaned)


def bytes_to_hex(data: bytes, sep: str = " ") -> str:
    """Convert bytes to uppercase hex string."""
    if not data:
        return ""
    hexed = data.hex().upper()
    if sep == "":
        return hexed
    return sep.join(hexed[i : i + 2] for i in range(0, len(hexed), 2))


def extract_json(text: str) -> dict:
    """
    Extract first JSON object from LLM response text.
    Handles: raw JSON, ```json fenced, embedded in prose.
    """
    if not isinstance(text, str):
        raise ValueError("text must be a string")

    fenced = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced:
        return json.loads(fenced.group(1))

    raw = text.strip()
    if raw.startswith("{") and raw.endswith("}"):
        return json.loads(raw)

    # Find first JSON object by brace matching
    start = raw.find("{")
    if start == -1:
        raise ValueError("no JSON object found")
    depth = 0
    for i in range(start, len(raw)):
        if raw[i] == "{":
            depth += 1
        elif raw[i] == "}":
            depth -= 1
            if depth == 0:
                return json.loads(raw[start : i + 1])
    raise ValueError("no complete JSON object found")


def validate_did(did: int) -> bool:
    """True if DID is in the valid 0x0000–0xFFFF range."""
    return isinstance(did, int) and 0x0000 <= did <= 0xFFFF


def validate_sid(sid: int) -> bool:
    """True if SID is a known UDS service."""
    return isinstance(sid, int) and sid in UDS_SERVICES


def build_alfid(addr_len: int, size_len: int) -> int:
    """Build addressAndLengthFormatIdentifier = (addrLen << 4) | sizeLen."""
    if not (0 <= addr_len <= 0x0F and 0 <= size_len <= 0x0F):
        raise ValueError("addr_len and size_len must be 0..15")
    return (addr_len << 4) | size_len


def split_dtc(dtc_3bytes: bytes) -> tuple[str, str]:
    """
    Parse 3-byte DTC representation into (category_letter, dtc_string).
    e.g. b'\x01\x23\x45' → ('P', 'P0123')
    """
    if not isinstance(dtc_3bytes, (bytes, bytearray)) or len(dtc_3bytes) != 3:
        raise ValueError("dtc_3bytes must be exactly 3 bytes")

    b1, b2, b3 = dtc_3bytes
    category_bits = (b1 & 0xC0) >> 6
    category_letter = {0: "P", 1: "C", 2: "B", 3: "U"}[category_bits]
    code = ((b1 & 0x3F) << 16) | (b2 << 8) | b3
    return category_letter, f"{category_letter}{code:04X}"


def dtc_status_summary(status_byte: int) -> str:
    """Return comma-separated active DTC status flag names."""
    if not isinstance(status_byte, int):
        raise ValueError("status_byte must be int")
    flags = [name for bit, name in DTC_STATUS_BITS.items() if status_byte & bit]
    return ", ".join(flags)


def suppress_pos_rsp(subfunc: int) -> int:
    """Set suppressPosRspMsgIndicationBit (bit 7) on a subFunction byte."""
    if not isinstance(subfunc, int):
        raise ValueError("subfunc must be int")
    return subfunc | 0x80


def positive_response_sid(request_sid: int) -> int:
    """Return request SID + 0x40."""
    if not isinstance(request_sid, int):
        raise ValueError("request_sid must be int")
    return request_sid + 0x40


def to_json(data: Any, indent: int = 2) -> str:
    """Serialize to JSON with stable formatting."""
    return json.dumps(data, indent=indent, ensure_ascii=False, default=str)


def to_yaml(data: Any) -> str:
    """Serialize to YAML (requires PyYAML)."""
    try:
        import yaml  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("PyYAML is required for YAML export") from exc
    return yaml.safe_dump(data, sort_keys=False)
