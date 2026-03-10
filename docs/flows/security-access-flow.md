# Security Access Flow

A step-by-step seed-key exchange walkthrough.

```python
from pyudskit import UDS

uds = UDS()
print(uds.security_access_flow(level=1))
```

!!! note "OEM algorithm"
    You must provide the OEM key algorithm to complete the flow.
