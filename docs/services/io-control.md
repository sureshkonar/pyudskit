# I/O Control Services

## InputOutputControlByIdentifier (0x2F)

Control actuators or signals identified by a DID.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x2F | Service identifier |
| 1–2 | dataIdentifier | DID | Target DID |
| 3 | controlOptionRecord | 0x00–0x03 | Control option |
| 4–N | controlState | bytes | Optional control data |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x6F | Positive response |
| 1–2 | dataIdentifier | echo | Echo DID |
| 3 | controlOptionRecord | echo | Echo option |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x31 | requestOutOfRange |
| 0x33 | securityAccessDenied |
| 0x7E | subFunctionNotSupportedInActiveSession |

### Subfunctions

| SubFunction | Name |
|---|---|
| 0x00 | returnControlToECU |
| 0x01 | resetToDefault |
| 0x02 | freezeCurrentState |
| 0x03 | shortTermAdjustment |

### Session Availability

Extended.

### pyuds Example

```python
from pyuds import UDS
uds = UDS()
print(uds.io_control(0x1234, "shortTermAdjustment", "FF")["uds_bytes"])  # 2F 12 34 03 FF
```

!!! warning "Actuator safety"
    I/O control can move actuators. Ensure the vehicle is safe before running tests.
