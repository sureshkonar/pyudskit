# Beginner Examples

## Read the VIN

```python
from pyudskit import UDS

uds = UDS()
print(uds.encode("Read the VIN"))
```

## Decode a negative response

```python
from pyudskit import UDS

uds = UDS()
print(uds.decode("7F 22 31"))
```

## Explain a DTC

```python
from pyudskit import UDS

uds = UDS()
print(uds.explain_dtc("P0301"))
```
