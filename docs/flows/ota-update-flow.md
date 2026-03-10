# OTA Update Flow

OTA software update using RequestFileTransfer (0x38).

```python
from pyuds import UDS

uds = UDS()
print(uds.ota_update_flow())
```

!!! warning "Authentication"
    OTA updates typically require authentication and signed packages.
