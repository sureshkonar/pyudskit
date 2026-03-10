# Advanced Examples

## Read multiple DIDs

```python
from pyuds import UDS

uds = UDS()
print(uds.read_dids([0xF190, 0xF186]))
```

## Read DTC snapshot

```python
from pyuds import UDS

uds = UDS()
print(uds.read_dtc_snapshot("01 23 45"))
```

## Routine control

```python
from pyuds import UDS

uds = UDS()
print(uds.routine_control(0xFF00, "start"))
```
