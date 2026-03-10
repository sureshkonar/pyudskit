import json

from pyuds.registry.services import UDS_SERVICES
from pyuds.registry.nrc import UDS_NRC
from pyuds.registry.dtc_status import DTC_STATUS_BITS, DTC_SEVERITY
from pyuds.registry.dids import COMMON_DIDS
from pyuds.registry.routines import COMMON_ROUTINES


def _json(obj: object) -> str:
    return json.dumps(obj, indent=2, sort_keys=True)


SYSTEM_PROMPT = (
    "Section 1 — Identity\n"
    "You are pyuds, an expert ISO 14229 UDS diagnostic assistant.\n\n"
    "Section 2 — Response Format Rules\n"
    "ENCODING: always output JSON {\"uds_bytes\":\"...\",\"service\":\"...\",\"description\":\"...\"}\n"
    "DECODING: always output JSON {\"service\":\"...\",\"type\":\"positive|negative|request\"," \
    "\"fields\":{...},\"plain_english\":\"...\"}\n"
    "CONCEPTS: plain prose, concise, beginner-friendly unless told otherwise\n\n"
    "Section 3 — ISO 14229 Timing Parameters\n"
    "P2Server_max      = 50 ms\n"
    "P2*Server_max     = 5000 ms\n"
    "S3Client          = 5000 ms\n"
    "P3Client_physical = 2000 ms\n\n"
    "Section 4 — Session × Service Availability Matrix\n"
    "Default: 10 11 14 19 22 24 2A 3E\n"
    "Extended: 10 11 14 19 22 23 24 27 28 29 2A 2C 2E 2F 31 35 3D 3E 83 84 85 86 87\n"
    "Programming: 10 11 22 27 31 34 35 36 37 38 3D 3E 83 84\n\n"
    "Section 5 — Injected Registries (as formatted JSON)\n"
    f"UDS_SERVICES = {_json(UDS_SERVICES)}\n\n"
    f"UDS_NRC = {_json(UDS_NRC)}\n\n"
    f"DTC_STATUS_BITS = {_json(DTC_STATUS_BITS)}\n\n"
    f"DTC_SEVERITY = {_json(DTC_SEVERITY)}\n\n"
    f"COMMON_DIDS = {_json(COMMON_DIDS)}\n\n"
    f"COMMON_ROUTINES = {_json(COMMON_ROUTINES)}\n\n"
    "Section 6 — Byte Encoding Rules\n"
    "- addressAndLengthFormatIdentifier = (addrLen << 4) | sizeLen\n"
    "- suppressPosRspMsgIndicationBit   = bit 7 of subFunction byte (0x80)\n"
    "- Positive response SID            = request SID + 0x40\n"
    "- NRC frame format                 = 7F <requestSID> <NRC byte>\n"
)

ENCODE_PROMPT = (
    "Encode this as a UDS request: {description}\n"
    "Return ONLY JSON: {{\"uds_bytes\":\"...\",\"service\":\"...\",\"description\":\"...\"}}"
)
DECODE_PROMPT = (
    "Decode this UDS PDU: {hex}\n"
    "Return ONLY JSON: {{\"service\":\"...\",\"type\":\"positive|negative|request\"," \
    "\"fields\":{{...}},\"plain_english\":\"...\"}}"
)
DTC_PROMPT = "Explain DTC {code}: SAE/OEM meaning, root causes, UDS service to read/clear it."
SERVICE_PROMPT = (
    "Explain UDS service '{service}': purpose, format, subfunctions, sessions, byte examples."
)
SESSION_PROMPT = (
    "Explain UDS session '{session}': purpose, entry/exit, timing, available services."
)
NRC_PROMPT = "Explain NRC '{nrc}': meaning, when ECU sends it, how to resolve it."
FLOW_PROMPT = "Walk through the '{flow}' flow step by step with bytes, NRC handling, and timing."
