# Decoding Responses

UDS responses can be cryptic. pyudskit decodes them into plain English.

```python
from pyudskit import UDS

uds = UDS()
print(uds.decode("7F 22 31"))
```

Expected output:

```python
Negative response: ReadDataByIdentifier was rejected (requestOutOfRange).
```

Use the full decoder for structured data:

```python
print(uds.decode_response("62 F1 90 57 30 4C 41 53 54 31 32 33 34 35 36 37 38"))
```

!!! note "RCRRP"
    If you receive `0x78`, wait for the ECU to respond with the final result.
