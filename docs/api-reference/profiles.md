# OEM Profiles

Profiles let you override DIDs, routines, services, and DTCs for a specific ECU/OEM.

```python
from pyudskit.profiles.loader import load_profile

profile = load_profile("pyudskit/profiles/oem_example.json")
print(profile.name)
```

```python
from pyudskit import UDS

uds = UDS(profile="pyudskit/profiles/oem_example.json")
print(uds.list_dids())
print(uds.explain_dtc("P0301"))
```

::: pyudskit.profiles.loader
::: pyudskit.profiles.schema
