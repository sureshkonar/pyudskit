# AI Client

`AIClient` is the LLM layer that wraps UDS services and returns structured JSON + plain English.

## Method Index

| Category | Methods |
|---|---|
| Encode/Decode | `encode`, `decode`, `explain_response` |
| DTC | `explain_dtc`, `explain_dtc_status` |
| Service | `explain_service`, `explain_service_result`, `verify_service_result` |
| NRC/Session | `explain_nrc`, `explain_session` |
| Flows | `get_flow` |
| Analysis | `analyze`, `compare`, `suggest_next_step` |
| Conversation | `chat`, `clear_history`, `reset` |

## Examples

```python
from pyudskit.ai import AIClient
from pyudskit.services import ReadDataByIdentifier

ai = AIClient()
svc = ReadDataByIdentifier()
req = svc.build_request([0xF190])

print(ai.explain_service_result(svc, req))
print(ai.verify_service_result(svc, req))
print(ai.decode("7F 22 31"))
```

## API Docs

::: pyudskit.ai.client.AIClient
