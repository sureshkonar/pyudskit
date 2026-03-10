# Data Transmission Services

## ReadDataByIdentifier (0x22)

Read the current value of one or more data records identified by a DID.

### Request Format

| Byte | Field | Value | Description |
|------|-------|-------|-------------|
| 0 | SID | 0x22 | Service identifier |
| 1–2 | dataIdentifier | e.g. 0xF190 | DID to read (2 bytes) |

### Response Format (Positive)

| Byte | Field | Value | Description |
|------|-------|-------|-------------|
| 0 | SID | 0x62 | Positive response (0x22 + 0x40) |
| 1–2 | dataIdentifier | e.g. 0xF190 | Echo of requested DID |
| 3–N | dataRecord | variable | Returned data |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x13 | incorrectMessageLengthOrInvalidFormat |
| 0x31 | requestOutOfRange |
| 0x7F | serviceNotSupportedInActiveSession |

### Subfunctions

None.

### Session Availability

Default, Extended, Programming (DID-dependent).

### pyuds Example

```python
from pyuds import UDS
uds = UDS()
result = uds.read_did(0xF190)
print(result["uds_bytes"])  # 22 F1 90
```

!!! warning "Session Required"
    ReadDataByIdentifier for some DIDs requires Extended session.

---

## ReadMemoryByAddress (0x23)

Read a block of memory at a specified address.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x23 | Service identifier |
| 1 | ALFID | (addrLen<<4)|sizeLen | Address/size format |
| 2–N | address + size | bytes | Address and length |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x63 | Positive response |
| 1–N | data | bytes | Memory contents |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x31 | requestOutOfRange |
| 0x22 | conditionsNotCorrect |

### Subfunctions

None.

### Session Availability

Extended, Programming.

### pyuds Example

```python
from pyuds import UDS
uds = UDS()
print(uds.read_memory(0x00001000, 0x10)["uds_bytes"])  # 23 44 ...
```

!!! warning "Address access"
    Memory access is heavily restricted and may require security.

---

## ReadScalingDataByIdentifier (0x24)

Read scaling/units for a DID.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x24 | Service identifier |
| 1–2 | dataIdentifier | DID | Target DID |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x64 | Positive response |
| 1–2 | dataIdentifier | echo | Echo DID |
| 3–N | scaling | bytes | Scaling data |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x31 | requestOutOfRange |
| 0x7F | serviceNotSupportedInActiveSession |

### Subfunctions

None.

### Session Availability

Default, Extended.

### pyuds Example

```python
from pyuds import UDS
uds = UDS()
print(uds.read_scaling_did(0xF186)["uds_bytes"])  # 24 F1 86
```

!!! warning "DID support"
    Not all ECUs implement scaling data for every DID.

---

## ReadDataByPeriodicIdentifier (0x2A)

Request periodic transmission of DIDs.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x2A | Service identifier |
| 1 | transmissionMode | 0x01–0x04 | Rate or stop |
| 2–N | DIDs | bytes | DIDs to transmit |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x6A | Positive response |
| 1 | transmissionMode | echo | Echo of request |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x31 | requestOutOfRange |
| 0x22 | conditionsNotCorrect |

### Subfunctions

| SubFunction | Name |
|---|---|
| 0x01 | stopSending |
| 0x02 | sendAtSlowRate |
| 0x03 | sendAtMediumRate |
| 0x04 | sendAtFastRate |

### Session Availability

Default, Extended.

### pyuds Example

```python
from pyuds import UDS
uds = UDS()
print(uds.encode("Send VIN periodically at slow rate"))
```

!!! warning "Bus load"
    Periodic data can increase bus utilization.

---

## DynamicallyDefineDataIdentifier (0x2C)

Create or clear dynamic DIDs.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x2C | Service identifier |
| 1 | subFunction | 0x01–0x03 | Define/clear |
| 2–N | data | bytes | Dynamic DID definition |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x6C | Positive response |
| 1 | subFunction | echo | Echo of request |
| 2–3 | dynamicDID | bytes | Dynamic DID |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x31 | requestOutOfRange |
| 0x22 | conditionsNotCorrect |

### Subfunctions

| SubFunction | Name |
|---|---|
| 0x01 | defineByIdentifier |
| 0x02 | defineByMemoryAddress |
| 0x03 | clearDynamicallyDefinedDataIdentifier |

### Session Availability

Extended.

### pyuds Example

```python
from pyuds import UDS
uds = UDS()
print(uds.define_dynamic_did(0xF200, [0xF190])["uds_bytes"])  # 2C 01 F2 00 F1 90
```

!!! warning "DID limits"
    ECUs may limit the number of dynamic DIDs.

---

## WriteDataByIdentifier (0x2E)

Write data to a DID.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x2E | Service identifier |
| 1–2 | dataIdentifier | DID | Target DID |
| 3–N | dataRecord | bytes | Data to write |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x6E | Positive response |
| 1–2 | dataIdentifier | echo | Echo DID |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x33 | securityAccessDenied |
| 0x31 | requestOutOfRange |

### Subfunctions

None.

### Session Availability

Extended, Programming.

### pyuds Example

```python
from pyuds import UDS
uds = UDS()
print(uds.write_did(0xF190, "31 32")["uds_bytes"])  # 2E F1 90 31 32
```

!!! warning "Security required"
    Many writable DIDs require SecurityAccess.

---

## WriteMemoryByAddress (0x3D)

Write a block of memory to a specified address.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x3D | Service identifier |
| 1 | ALFID | (addrLen<<4)|sizeLen | Address format |
| 2–N | address + data | bytes | Address and data |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x7D | Positive response |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x33 | securityAccessDenied |
| 0x31 | requestOutOfRange |

### Subfunctions

None.

### Session Availability

Programming.

### pyuds Example

```python
from pyuds import UDS
uds = UDS()
print(uds.write_memory(0x00001000, "AA BB")["uds_bytes"])  # 3D 40 ...
```

!!! warning "Dangerous"
    Writing memory can brick the ECU if used incorrectly.
