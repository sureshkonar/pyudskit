# DTC Status Bits

| Bit | Mask | Name | Meaning |
|---|---|---|---|
| 0 | 0x01 | testFailed | Test failed |
| 1 | 0x02 | testFailedThisMonitoringCycle | Failed this cycle |
| 2 | 0x04 | pendingDTC | Pending DTC |
| 3 | 0x08 | confirmedDTC | Confirmed DTC |
| 4 | 0x10 | testNotCompletedSinceLastClear | Not completed since clear |
| 5 | 0x20 | testFailedSinceLastClear | Failed since clear |
| 6 | 0x40 | testNotCompletedThisMonitoringCycle | Not completed this cycle |
| 7 | 0x80 | warningIndicatorRequested | MIL requested |

```python
from pyuds import UDS

uds = UDS()
print(uds.decode_dtc_status(0x2C))
```
