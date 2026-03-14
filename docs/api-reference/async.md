# Async API

`AsyncUDS` provides async wrappers for all UDS methods.

```python
import asyncio
from pyudskit.async_client import AsyncUDS

async def main():
    uds = AsyncUDS()
    print(await uds.encode("Read the VIN"))

asyncio.run(main())
```

::: pyudskit.async_client.AsyncUDS
