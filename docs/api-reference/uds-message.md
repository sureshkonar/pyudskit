# UDSMessage

The `UDSMessage` dataclass parses and validates a single UDS PDU.

```python
from pyuds.message import UDSMessage

msg = UDSMessage.from_hex("62 F1 90")
print(msg.service_name)
```

::: pyuds.message.UDSMessage
