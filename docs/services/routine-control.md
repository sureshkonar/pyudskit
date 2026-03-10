# Routine Control Services

## RoutineControl (0x31)

Start, stop, or read results from an ECU routine.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x31 | Service identifier |
| 1 | subFunction | 0x01/0x02/0x03 | Start/Stop/Result |
| 2–3 | routineIdentifier | bytes | Routine ID |
| 4–N | data | bytes | Optional routine data |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x71 | Positive response |
| 1 | subFunction | echo | Echo of request |
| 2–3 | routineIdentifier | echo | Routine ID |
| 4–N | data | bytes | Optional routine data |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x31 | requestOutOfRange |
| 0x33 | securityAccessDenied |

### Subfunctions

| SubFunction | Name |
|---|---|
| 0x01 | startRoutine |
| 0x02 | stopRoutine |
| 0x03 | requestRoutineResults |

### Session Availability

Extended, Programming.

### pyudskit Example

```python
from pyudskit import UDS
uds = UDS()
print(uds.routine_control(0xFF00, "start")["uds_bytes"])  # 31 01 FF 00
```

!!! warning "Routine dependencies"
    Many routines require specific sessions and security levels.
