# Transport

Transport adapters enable real ECU I/O over CAN and DoIP.

## Components

- `Transport` base class
- `CANTransport` (python-can)
- `DoIPTransport` (doipy)
- `IsoTpSegmenter` / `IsoTpReassembler`
- `UDSTransportClient` (request/response session)
- `MockTransport` (tests/sim)

## Example

```python
from pyudskit.transport import CANTransport

tr = CANTransport(channel="can0", bustype="socketcan", rx_id=0x7E8, tx_id=0x7E0)
tr.send(bytes.fromhex("22 F1 90"))
resp = tr.recv(2000)
print(resp)
tr.close()
```

```python
from pyudskit.transport import UDSTransportClient, MockTransport

mock = MockTransport(responses=[bytes.fromhex("50 03 00 19 01 F4")])
client = UDSTransportClient(mock)
print(client.request(bytes.fromhex("10 03")))
```

## API Docs

::: pyudskit.transport
::: pyudskit.transport.base.Transport
::: pyudskit.transport.can.CANTransport
::: pyudskit.transport.doip.DoIPTransport
::: pyudskit.transport.isotp.IsoTpSegmenter
::: pyudskit.transport.isotp.IsoTpReassembler
::: pyudskit.transport.session.UDSTransportClient
::: pyudskit.transport.session.UDSTiming
::: pyudskit.transport.mock.MockTransport
