# Diagnostic Trouble Codes (DTCs)

## What is a DTC?

A Diagnostic Trouble Code is a standardized identifier for a fault condition. Technicians use DTCs to understand which system reported a problem.

## SAE J2012 format

Example: `P0301`

- **P** = Powertrain
- **0** = SAE standard
- **3** = Ignition system or misfire
- **01** = Cylinder 1

## DTC categories

| Prefix | Category |
|---|---|
| P | Powertrain |
| C | Chassis |
| B | Body |
| U | Network / Communication |

## DTC status byte

```python
Bit 7  Bit 6  Bit 5  Bit 4  Bit 3  Bit 2  Bit 1  Bit 0
WIR    TNCMC  TFSLC  TNCSLC  CDTC  PDTC   TFTMC  TF
```

- **TF**: testFailed
- **TFTMC**: testFailedThisMonitoringCycle
- **PDTC**: pendingDTC
- **CDTC**: confirmedDTC
- **TNCSLC**: testNotCompletedSinceLastClear
- **TFSLC**: testFailedSinceLastClear
- **TNCMC**: testNotCompletedThisMonitoringCycle
- **WIR**: warningIndicatorRequested

## Pending vs confirmed

- **Pending**: fault detected but not confirmed.
- **Confirmed**: fault verified across cycles.
- **Permanent**: stored by emission rules in some systems.

## Snapshot and extended data

- Snapshot (freeze frame) captures data at the time of failure.
- Extended data provides additional state and counters.

## pyudskit usage

```python
from pyudskit import UDS

uds = UDS()
print(uds.read_dtcs())
print(uds.explain_dtc("P0301"))
print(uds.decode_dtc_status(0x2C))
```
