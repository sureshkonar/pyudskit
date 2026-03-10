# I/O Control Flow

A walkthrough of I/O control options.

```python
from pyuds import UDS

uds = UDS()
print(uds.io_control_flow(0x1234))
```

!!! warning "Actuator safety"
    Ensure the vehicle is safe before commanding actuators.
