# Reading DTCs

Read Diagnostic Trouble Codes with a single method call.

```python
from pyuds import UDS

uds = UDS()
result = uds.read_dtcs(0x08)
print(result["uds_bytes"])  # 19 02 08
```

If your ECU returns DTCs, you can decode each one:

```python
print(uds.explain_dtc("P0301"))
```

!!! warning "Session requirements"
    Some ECUs require an extended session to read DTCs. Use `uds.switch_session("extended")` if needed.
