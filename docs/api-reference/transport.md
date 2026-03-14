# Transport

Transport adapters enable real ECU I/O over CAN and DoIP.

## Components

- `Transport` base class
- `CANTransport` (python-can)
- `DoIPTransport` (doipy)
- `IsoTpSegmenter` / `IsoTpReassembler`

## Example

```python
from pyudskit.transport import CANTransport

tr = CANTransport(channel="can0", bustype="socketcan", rx_id=0x7E8, tx_id=0x7E0)
tr.send(bytes.fromhex("22 F1 90"))
resp = tr.recv(2000)
print(resp)
tr.close()
```

## API Docs

::: pyudskit.transport
::: pyudskit.transport.base.Transport
::: pyudskit.transport.can.CANTransport
::: pyudskit.transport.doip.DoIPTransport
::: pyudskit.transport.isotp.IsoTpSegmenter
::: pyudskit.transport.isotp.IsoTpReassembler
