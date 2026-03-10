# DTC Management Services

## ClearDiagnosticInformation (0x14)

Clear stored DTCs by group.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x14 | Service identifier |
| 1–3 | groupOfDTC | 3 bytes | DTC group or `FF FF FF` |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x54 | Positive response |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x22 | conditionsNotCorrect |
| 0x31 | requestOutOfRange |

### Subfunctions

None.

### Session Availability

Default, Extended.

### pyudskit Example

```python
from pyudskit import UDS
uds = UDS()
print(uds.clear_dtcs()["uds_bytes"])  # 14 FF FF FF
```

!!! warning "Data loss"
    Clearing DTCs also clears related freeze frame data.

---

## ReadDTCInformation (0x19)

Read DTCs, status, snapshot data, and extended records.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x19 | Service identifier |
| 1 | subFunction | 0x01–0x15 | Report type |
| 2–N | parameters | bytes | Subfunction parameters |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x59 | Positive response |
| 1 | subFunction | echo | Echo of request |
| 2–N | data | bytes | DTC data |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x13 | incorrectMessageLengthOrInvalidFormat |
| 0x31 | requestOutOfRange |
| 0x22 | conditionsNotCorrect |

### Subfunctions

| SubFunction | Name |
|---|---|
| 0x01 | reportNumberOfDTCByStatusMask |
| 0x02 | reportDTCByStatusMask |
| 0x03 | reportDTCSnapshotIdentification |
| 0x04 | reportDTCSnapshotRecordByDTCNumber |
| 0x05 | reportDTCExtDataRecordByDTCNumber |
| 0x06 | reportNumberOfDTCBySeverityMaskRecord |
| 0x07 | reportDTCBySeverityMaskRecord |
| 0x08 | reportSeverityInformationOfDTC |
| 0x09 | reportSupportedDTC |
| 0x0A | reportAllSupportedDTC |
| 0x0B | reportFirstTestFailedDTC |
| 0x0C | reportFirstConfirmedDTC |
| 0x0D | reportMostRecentTestFailedDTC |
| 0x0E | reportMostRecentConfirmedDTC |
| 0x0F | reportMirrorMemoryDTCByStatusMask |
| 0x10 | reportMirrorMemoryDTCExtDataRecordByDTCNumber |
| 0x11 | reportNumberOfMirrorMemoryDTCByStatusMask |
| 0x12 | reportNumberOfEmissionsRelatedOBDDTCByStatusMask |
| 0x13 | reportEmissionsRelatedOBDDTCByStatusMask |
| 0x14 | reportDTCFaultDetectionCounter |
| 0x15 | reportDTCWithPermanentStatus |

### Session Availability

Default, Extended.

### pyudskit Example

```python
from pyudskit import UDS
uds = UDS()
print(uds.read_dtcs(0x08)["uds_bytes"])  # 19 02 08
```

!!! warning "Large responses"
    DTC lists can exceed single-frame limits. Use a transport that supports multi-frame responses.
