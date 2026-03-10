# Negative Response Codes (NRCs)

When a request fails, the ECU returns a negative response frame:

```python
7F <requestSID> <NRC>
```

Common examples:

- `0x11` serviceNotSupported
- `0x22` conditionsNotCorrect
- `0x31` requestOutOfRange
- `0x78` requestCorrectlyReceivedResponsePending (RCRRP)

## How to handle NRCs

1. Identify the request SID.
2. Look up the NRC meaning.
3. Fix session/security/sequence issues.
4. Retry if appropriate.

!!! warning "RCRRP (0x78)"
    The ECU accepted your request but needs more time. Keep waiting and retry the request or wait for the final response.

pyudskit provides:

- `uds.explain_nrc("0x22")`
- `uds.lookup_nrc(0x78)`
- Full NRC registry in `pyudskit.registry.nrc`
