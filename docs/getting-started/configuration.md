# Configuration

## Basic Options

```python
from pyudskit import UDS

uds = UDS(
    api_key="sk-ant-...",
    model="claude-sonnet-4-20250514",
    verbose=False,
)
```

- `api_key`: overrides `ANTHROPIC_API_KEY`.
- `model`: choose an Anthropic model.
- `verbose`: prints raw LLM output for debugging.

## Session State

pyudskit tracks ECU context automatically:

```python
uds.switch_session("extended")
uds.security_access_seed(level=1)
print(uds.ecu_state)
```

## Advanced Overrides

If you need a fresh context:

```python
uds.clear_session()
```

## Related References

- API Reference → AI Client
- API Reference → Services
- API Reference → Transport
- API Reference → Async
- API Reference → CLI
- API Reference → OEM Profiles

!!! tip "Testing"
    Use the test fixtures in `tests/conftest.py` to mock LLM responses.
