# Utils

Helper utilities for parsing hex, DTC status bits, and DID/SID validation.

```python
from pyudskit.utils import parse_hex, bytes_to_hex, to_json, to_yaml

print(parse_hex("22 F1 90"))
print(bytes_to_hex(b"\x22\xF1\x90"))
print(to_json({"ok": True}))
print(to_yaml({"ok": True}))
```

::: pyudskit.utils
