# UDS Services

UDS services are standardized commands identified by a **Service ID (SID)**. Each service has a request and a positive response SID (request + 0x40).

Examples:

- `0x10` DiagnosticSessionControl
- `0x22` ReadDataByIdentifier
- `0x19` ReadDTCInformation

Services are grouped by purpose: session management, data transmission, DTC management, I/O control, routine control, and upload/download.

pyudskit provides:

- Beginner methods like `encode()` and `decode()`
- Service shortcuts like `read_did()` and `read_dtcs()`
- Full registries in `pyudskit.registry` for validation and lookup

!!! note "Positive response SID"
    A positive response uses `request SID + 0x40`. For example, `0x22` → `0x62`.
