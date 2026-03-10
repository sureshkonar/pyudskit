# pyuds — Talk to your ECU in plain English

[Get Started](getting-started/installation.md){ .md-button .md-button--primary }
[API Reference](api-reference/uds-class.md){ .md-button }
[GitHub](https://github.com/your-org/pyuds){ .md-button }

---

## What is pyuds?

pyuds is a Python library that brings AI to automotive diagnostics. It wraps the full ISO 14229 UDS (Unified Diagnostic Services) standard and lets you interact with ECUs using plain English — powered by Claude LLM.

## At a Glance

| Feature | Details |
|---|---|
| Standard | ISO 14229-1 (UDS), ISO 15765, ISO 13400 DoIP |
| Services | All 26+ ISO 14229 services |
| DTC Codes | P / C / B / U — explain, read, clear |
| Audiences | Beginners & advanced engineers |
| Backend | Anthropic Claude (claude-sonnet-4-20250514) |
| Python | 3.10+ |

## Install

```python
pip install pyuds
```

## 30-Second Demo

```python
from pyuds import UDS

uds = UDS()

print(uds.encode("Read the VIN"))
print(uds.decode("62 F1 90 57 30 4C 41 53 54 31 32 33 34 35 36 37 38"))
print(uds.explain_dtc("P0301"))
print(uds.programming_flow())
```

## Why pyuds?

| Beginner Friendly | Full ISO 14229 | LLM Powered |
|---|---|---|
| Plain English I/O | All 26+ services | Claude backend |
| One-liners | 40+ NRCs | Multi-turn context |
| Built-in help() | 0xF1xx DIDs | Byte-accurate |
