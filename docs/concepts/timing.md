# Timing Parameters

UDS timing parameters control how quickly requests and responses occur.

| Parameter | Typical Value | Meaning |
|---|---|---|
| P2Server_max | 50 ms | Normal response time limit |
| P2*Server_max | 5000 ms | Extended response time after RCRRP |
| S3Client | 5000 ms | Session keep-alive interval |
| P3Client_physical | 2000 ms | Inter-message timing |

## Why timing matters

If you violate timing requirements, ECUs may return NRC `0x21` (busyRepeatRequest) or `0x78` (responsePending).

## pyuds behavior

pyuds surfaces these values in the system prompt to improve LLM reasoning and can be used in flow explanations.
