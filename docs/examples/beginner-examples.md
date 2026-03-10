# Beginner Examples

## Read the VIN

```python
from pyuds import UDS

uds = UDS()
print(uds.encode("Read the VIN"))
```

## Decode a negative response

```python
from pyuds import UDS

uds = UDS()
print(uds.decode("7F 22 31"))
```

## Explain a DTC

```python
from pyuds import UDS

uds = UDS()
print(uds.explain_dtc("P0301"))
```
