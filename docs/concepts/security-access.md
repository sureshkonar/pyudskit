# Security Access

SecurityAccess (0x27) prevents unauthorized ECU modification. It uses a **seed–key** challenge-response flow.

## How it works

1. Tester requests a seed (`0x27` odd subfunction).
2. ECU responds with a seed.
3. Tester computes a key using an OEM algorithm.
4. Tester sends the key (`0x27` even subfunction).

## Subfunction rules

- **Odd** = request seed (1, 3, 5, ...)
- **Even** = send key (2, 4, 6, ...)

## Common key algorithms

OEMs typically use proprietary logic. Simple systems may use XOR or additive transforms; advanced systems use HMAC or crypto hardware.

## Timing and lockouts

After multiple failures, ECUs often enforce a delay (NRC `0x37`).

## Common NRCs

- `0x35` invalidKey
- `0x36` exceedNumberOfAttempts
- `0x37` requiredTimeDelayNotExpired

## Annotated walkthrough

```python
Request seed:     27 01
ECU response:     67 01 A3 F2 C1 09   ← seed = A3F2C109
Calculate key:    [your algorithm]
Send key:         27 02 5C 0D 3E F6
ECU response:     67 02               ← access granted
```

## pyudskit example

```python
from pyudskit import UDS

uds = UDS()
print(uds.security_access_flow(level=1))
```

## Custom Key Algorithm

```python
from pyudskit import UDS

def xor_algo(seed: bytes, level: int) -> bytes:
    return bytes(b ^ 0xAA for b in seed)

uds = UDS()
uds.register_security_algorithm("xor", xor_algo)
print(uds.security_access_key_from_seed(1, "A3 F2 C1 09", "xor"))
```
