# DTC Reading Flow

A complete DTC read + snapshot + extended data + clear workflow.

```python
from pyudskit import UDS

uds = UDS()
print(uds.dtc_reading_flow())
```

!!! tip "Status mask"
    Start with `0x08` to read confirmed DTCs, then expand as needed.
