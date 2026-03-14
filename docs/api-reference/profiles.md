# OEM Profiles

Profiles let you override DIDs, routines, and service metadata for a specific ECU/OEM.

```python
from pyudskit.profiles.loader import load_profile

profile = load_profile("pyudskit/profiles/oem_example.json")
print(profile.name)
```

::: pyudskit.profiles.loader
::: pyudskit.profiles.schema
