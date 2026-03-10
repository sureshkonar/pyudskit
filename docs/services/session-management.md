# Session Management Services

## DiagnosticSessionControl (0x10)

Switch the ECU between default, programming, and extended sessions.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x10 | Service identifier |
| 1 | subFunction | 0x01/0x02/0x03 | Session type |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x50 | Positive response |
| 1 | subFunction | echo | Echo of request |
| 2–3 | P2ServerMax | ms | Normal response timing |
| 4–5 | P2*ServerMax | ms | Extended response timing |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x12 | subFunctionNotSupported |
| 0x7E | subFunctionNotSupportedInActiveSession |
| 0x22 | conditionsNotCorrect |

### Subfunctions

| SubFunction | Name |
|---|---|
| 0x01 | defaultSession |
| 0x02 | programmingSession |
| 0x03 | extendedDiagnosticSession |

### Session Availability

All sessions.

### pyudskit Example

```python
from pyudskit import UDS

uds = UDS()
print(uds.switch_session("extended")["uds_bytes"])  # 10 03
```

!!! warning "Session resets"
    Some ECUs reset timers and disable services after session switches. Use `TesterPresent` to keep the session alive.

---

## ECUReset (0x11)

Request a reset of the ECU.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x11 | Service identifier |
| 1 | resetType | 0x01/0x02/0x03 | Hard/KeyOffOn/Soft |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x51 | Positive response |
| 1 | resetType | echo | Echo of request |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x12 | subFunctionNotSupported |
| 0x22 | conditionsNotCorrect |

### Subfunctions

| SubFunction | Name |
|---|---|
| 0x01 | hardReset |
| 0x02 | keyOffOnReset |
| 0x03 | softReset |

### Session Availability

All sessions.

### pyudskit Example

```python
from pyudskit import UDS

uds = UDS()
print(uds.ecu_reset("hard")["uds_bytes"])  # 11 01
```

!!! warning "Side effects"
    ECU reset may drop the connection. Reconnect before sending further requests.

---

## SecurityAccess (0x27)

Unlocks protected services via seed-key exchange.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x27 | Service identifier |
| 1 | subFunction | odd/even | Seed request or key send |
| 2–N | data | seed/key | Optional key bytes |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x67 | Positive response |
| 1 | subFunction | echo | Echo of request |
| 2–N | seed | bytes | Seed for key calculation |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x35 | invalidKey |
| 0x36 | exceedNumberOfAttempts |
| 0x37 | requiredTimeDelayNotExpired |

### Subfunctions

| SubFunction | Name |
|---|---|
| 0x01 | requestSeedLevel1 |
| 0x02 | sendKeyLevel1 |
| 0x03 | requestSeedLevel2 |
| 0x04 | sendKeyLevel2 |
| 0x05 | requestSeedLevel3 |
| 0x06 | sendKeyLevel3 |

### Session Availability

Extended, Programming.

### pyudskit Example

```python
from pyudskit import UDS

uds = UDS()
print(uds.security_access_seed(level=1)["uds_bytes"])  # 27 01
```

!!! warning "OEM algorithm"
    Key calculation is OEM-specific. pyudskit does not ship OEM secrets.

---

## CommunicationControl (0x28)

Enable or disable ECU communication.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x28 | Service identifier |
| 1 | subFunction | 0x00–0x03 | Rx/Tx control |
| 2 | commType | 0x01 | Application network |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x68 | Positive response |
| 1 | subFunction | echo | Echo of request |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x12 | subFunctionNotSupported |
| 0x31 | requestOutOfRange |

### Subfunctions

| SubFunction | Name |
|---|---|
| 0x00 | enableRxAndTx |
| 0x01 | enableRxDisableTx |
| 0x02 | disableRxEnableTx |
| 0x03 | disableRxAndTx |

### Session Availability

Extended.

### pyudskit Example

```python
from pyudskit import UDS

uds = UDS()
print(uds.communication_control("disable")["uds_bytes"])  # 28 03 01
```

!!! warning "Loss of comms"
    Disabling Rx/Tx may block future requests until reset.

---

## Authentication (0x29)

ISO 14229-1:2020 authentication services.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x29 | Service identifier |
| 1 | subFunction | 0x01–0x03 | Auth steps |
| 2–N | data | bytes | Auth data |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x69 | Positive response |
| 1 | subFunction | echo | Echo of request |
| 2–N | data | bytes | Auth response |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x34 | authenticationRequired |
| 0x50–0x5D | certificate/auth errors |

### Subfunctions

| SubFunction | Name |
|---|---|
| 0x01 | requestChallenge |
| 0x02 | verifyResponse |
| 0x03 | authenticationComplete |

### Session Availability

Extended, Programming.

### pyudskit Example

```python
from pyudskit import UDS

uds = UDS()
print(uds.encode("Authenticate with ECU"))
```

!!! warning "Certificate flow"
    Authentication requires ECU-specific credentials and certificates.

---

## TesterPresent (0x3E)

Keep-alive to avoid session timeout.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x3E | Service identifier |
| 1 | subFunction | 0x00 or 0x80 | 0x80 suppresses positive response |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x7E | Positive response |
| 1 | subFunction | echo | Echo of request |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x11 | serviceNotSupported |

### Subfunctions

| SubFunction | Name |
|---|---|
| 0x00 | zeroSubFunction |

### Session Availability

All sessions.

### pyudskit Example

```python
from pyudskit import UDS

uds = UDS()
print(uds.tester_present()["uds_bytes"])  # 3E 80
```

!!! warning "Suppress positive response"
    Some gateways ignore suppressed responses. Disable suppression if needed.

---

## AccessTimingParameter (0x83)

Read or set ECU timing parameters.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x83 | Service identifier |
| 1 | subFunction | 0x01–0x03 | Timing operation |
| 2–N | data | bytes | Optional timing data |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0xC3 | Positive response |
| 1 | subFunction | echo | Echo of request |
| 2–N | data | bytes | Timing data |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x31 | requestOutOfRange |
| 0x22 | conditionsNotCorrect |

### Subfunctions

| SubFunction | Name |
|---|---|
| 0x01 | readExtendedTimingParameterSet |
| 0x02 | setTimingParametersToDefault |
| 0x03 | readCurrentlyActiveTimingParameters |

### Session Availability

Extended.

### pyudskit Example

```python
from pyudskit import UDS

uds = UDS()
print(uds.encode("Read currently active timing parameters"))
```

!!! warning "Timing mismatch"
    Incorrect timing parameters may break communication.

---

## SecuredDataTransmission (0x84)

Transmit secured data blocks.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x84 | Service identifier |
| 1–N | data | bytes | Secured payload |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0xC4 | Positive response |
| 1–N | data | bytes | Response data |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x38 | secureDataTransmissionRequired |
| 0x39 | secureDataTransmissionNotAllowed |

### Session Availability

Extended, Programming.

### pyudskit Example

```python
from pyudskit import UDS

uds = UDS()
print(uds.encode("Send secured data block"))
```

!!! warning "Security policy"
    Requires ECU-specific security provisioning.

---

## ControlDTCSetting (0x85)

Enable or disable DTC setting.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x85 | Service identifier |
| 1 | subFunction | 0x01/0x02 | On/Off |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0xC5 | Positive response |
| 1 | subFunction | echo | Echo of request |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x7E | subFunctionNotSupportedInActiveSession |

### Subfunctions

| SubFunction | Name |
|---|---|
| 0x01 | on |
| 0x02 | off |

### Session Availability

Extended.

### pyudskit Example

```python
from pyudskit import UDS

uds = UDS()
print(uds.control_dtc_setting("off")["uds_bytes"])  # 85 02
```

!!! warning "Diagnostics impact"
    Turning off DTC setting can hide faults. Use with care.

---

## ResponseOnEvent (0x86)

Configure ECU to respond on specific events.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x86 | Service identifier |
| 1 | subFunction | 0x00–0x03 | Event type |
| 2–N | data | bytes | Event configuration |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0xC6 | Positive response |
| 1 | subFunction | echo | Echo of request |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x12 | subFunctionNotSupported |
| 0x31 | requestOutOfRange |

### Subfunctions

| SubFunction | Name |
|---|---|
| 0x00 | stopResponseOnEvent |
| 0x01 | onDTCStatusChange |
| 0x02 | onTimer |
| 0x03 | onChangeOfDataIdentifier |

### Session Availability

Extended.

### pyudskit Example

```python
from pyudskit import UDS

uds = UDS()
print(uds.encode("Configure response on DTC status change"))
```

!!! warning "Event load"
    Excessive event reporting can overload the bus.

---

## LinkControl (0x87)

Control link-layer parameters such as baud rate.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x87 | Service identifier |
| 1 | subFunction | 0x01/0x02 | Verify/Transition |
| 2 | baudrateIdentifier | byte | New speed |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0xC7 | Positive response |
| 1 | subFunction | echo | Echo of request |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x31 | requestOutOfRange |
| 0x22 | conditionsNotCorrect |

### Subfunctions

| SubFunction | Name |
|---|---|
| 0x01 | verifyBaudrateTransition |
| 0x02 | transitionBaudrate |

### Session Availability

Extended.

### pyudskit Example

```python
from pyudskit import UDS

uds = UDS()
print(uds.encode("Verify baudrate transition to 500k"))
```

!!! warning "Loss of communication"
    Changing baud rate can drop the link. Ensure both sides change together.
