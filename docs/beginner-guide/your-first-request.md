# Your First Request

This guide sends your first UDS request using plain English.

```python
from pyudskit import UDS

uds = UDS()
print(uds.encode("Read the VIN"))
```

Expected output:

```python
22 F1 90
```

Explanation: the LLM turns your request into UDS bytes for `ReadDataByIdentifier` and DID `0xF190` (VIN).

!!! tip "Next step"
    Use `uds.decode(...)` to interpret the response bytes you receive from an ECU.
