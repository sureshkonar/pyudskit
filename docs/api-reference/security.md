# Security Algorithms

Register custom seed-key algorithms for `SecurityAccess`.

```python
from pyudskit import UDS

uds = UDS()
uds.register_security_algorithm("xor", lambda seed, level: bytes(b ^ 0xAA for b in seed))
print(uds.list_security_algorithms())
```

::: pyudskit.security
