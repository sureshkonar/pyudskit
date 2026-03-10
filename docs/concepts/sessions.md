# Diagnostic Sessions

A diagnostic session controls which services are available and what security is required.

## Why sessions exist

ECUs restrict dangerous operations (programming, IO control) to special sessions. This prevents accidental or unauthorized changes.

## Standard sessions

| Session | SID | Purpose | Security Required |
|---|---|---|---|
| Default (0x01) | `10 01` | Basic diagnostics, read DTCs | No |
| Programming (0x02) | `10 02` | ECU flashing | Yes (SecurityAccess) |
| Extended (0x03) | `10 03` | Advanced diagnostics, I/O control | Sometimes |

## Timeouts

UDS sessions time out if no traffic is received. The standard keep-alive is **S3 = 5000 ms**. Use `TesterPresent` (0x3E) to keep the session alive.

## Session transitions

<!-- Diagram: Default → Extended → Programming -->

## pyudskit example

```python
from pyudskit import UDS

uds = UDS()
uds.switch_session("extended")
print(uds.ecu_state)
```

!!! tip "Session support"
    If you receive NRC `0x7F` or `0x7E`, switch to the correct session before retrying.
