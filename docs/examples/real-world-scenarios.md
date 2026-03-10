# Real-World Scenarios

## Scenario 1 — Workshop DTC Scan

```python
from pyudskit import UDS

uds = UDS()

# Read confirmed DTCs
result = uds.read_dtcs(0x08)
print(result["uds_bytes"])

# Explain a few known DTCs
for code in ["P0301", "U0100", "B0020"]:
    print(uds.explain_dtc(code))

# Clear all DTCs after repair
print(uds.clear_dtcs())
```

## Scenario 2 — ECU Software Update

```python
from pyudskit import UDS

uds = UDS()

uds.switch_session("extended")
uds.communication_control("disable")
uds.control_dtc_setting("off")
uds.security_access_flow(level=1)
uds.switch_session("programming")
uds.routine_control(0xFF00, "start")  # erase
uds.request_download(0x08000000, 0x10000)
uds.transfer_data(0x01, "AA BB CC ...")
uds.request_transfer_exit()
uds.ecu_reset("hard")
```

## Scenario 3 — End-of-Line Configuration

```python
from pyudskit import UDS

uds = UDS()

uds.switch_session("extended")
uds.security_access_flow(level=1)
uds.routine_control(0xF000, "start", "01 02 03")  # variant coding
print(uds.lookup_did(0xF190))
```

## Scenario 4 — Actuator Test

```python
from pyudskit import UDS

uds = UDS()

uds.switch_session("extended")
uds.security_access_flow(level=1)
print(uds.io_control(0x1234, "shortTermAdjustment", "FF"))
print(uds.io_control(0x1234, "returnControlToECU"))
```

## Scenario 5 — Reading Live Data

```python
from pyudskit import UDS

uds = UDS()

print(uds.read_did(0xF190))  # VIN
print(uds.read_did(0xF18C))  # ECU serial number
print(uds.read_did(0xF184))  # software version
print(uds.read_did(0xF186))  # active session
```
