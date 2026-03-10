# Data Identifiers (DIDs)

DIDs are standardized identifiers for ECU data. They are read using **ReadDataByIdentifier (0x22)** and optionally written with **WriteDataByIdentifier (0x2E)**.

Common DIDs in the 0xF1xx range include VIN, software versions, and serial numbers.

## Example: Read VIN

```python
from pyuds import UDS

uds = UDS()
result = uds.read_did(0xF190)
print(result["uds_bytes"])  # 22 F1 90
```

!!! tip "Multiple DIDs"
    You can read multiple DIDs in a single request with `uds.read_dids([0xF190, 0xF186])`.
