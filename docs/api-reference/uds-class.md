# UDS Class

## Method Index

| Category | Methods |
|---|---|
| Beginner | `ask`, `encode`, `decode`, `explain_dtc`, `explain_service`, `help` |
| Encoding | `encode_request`, `decode_response` |
| Data | `read_did`, `write_did`, `read_memory`, `write_memory` |
| DTC | `read_dtcs`, `clear_dtcs`, `read_dtc_snapshot`, `read_dtc_extended` |
| Session | `switch_session`, `ecu_reset`, `tester_present` |
| Security | `security_access_seed`, `security_access_key` |
| Routine | `routine_control` |
| Flash | `request_download`, `transfer_data`, `request_transfer_exit` |
| Flows | `programming_flow`, `security_access_flow`, `dtc_reading_flow` |
| Utils | `list_services`, `lookup_nrc`, `clear_session`, `ecu_state` |

## Examples Per Method

### ask

```python
from pyuds import UDS
uds = UDS()
print(uds.ask("What is UDS?"))
```

### encode

```python
from pyuds import UDS
uds = UDS()
print(uds.encode("Read the VIN"))  # 22 F1 90
```

### decode

```python
from pyuds import UDS
uds = UDS()
print(uds.decode("7F 22 31"))
```

### explain_dtc

```python
from pyuds import UDS
uds = UDS()
print(uds.explain_dtc("P0301"))
```

### explain_service

```python
from pyuds import UDS
uds = UDS()
print(uds.explain_service("0x27"))
```

### explain_session

```python
from pyuds import UDS
uds = UDS()
print(uds.explain_session("programming"))
```

### explain_nrc

```python
from pyuds import UDS
uds = UDS()
print(uds.explain_nrc("0x22"))
```

### decode_dtc_status

```python
from pyuds import UDS
uds = UDS()
print(uds.decode_dtc_status(0x2C))
```

### lookup_did

```python
from pyuds import UDS
uds = UDS()
print(uds.lookup_did(0xF190))
```

### help

```python
from pyuds import UDS
uds = UDS()
uds.help()
```

### encode_request

```python
from pyuds import UDS
uds = UDS()
print(uds.encode_request("Read the VIN"))
```

### decode_response

```python
from pyuds import UDS
uds = UDS()
print(uds.decode_response("62 F1 90 57 30 4C 41 53 54"))
```

### read_did

```python
from pyuds import UDS
uds = UDS()
print(uds.read_did(0xF190))
```

### read_dids

```python
from pyuds import UDS
uds = UDS()
print(uds.read_dids([0xF190, 0xF186]))
```

### write_did

```python
from pyuds import UDS
uds = UDS()
print(uds.write_did(0xF190, "31 32 33"))
```

### read_memory

```python
from pyuds import UDS
uds = UDS()
print(uds.read_memory(0x00001000, 0x10))
```

### write_memory

```python
from pyuds import UDS
uds = UDS()
print(uds.write_memory(0x00001000, "AA BB"))
```

### read_scaling_did

```python
from pyuds import UDS
uds = UDS()
print(uds.read_scaling_did(0xF186))
```

### define_dynamic_did

```python
from pyuds import UDS
uds = UDS()
print(uds.define_dynamic_did(0xF200, [0xF190]))
```

### clear_dynamic_did

```python
from pyuds import UDS
uds = UDS()
print(uds.clear_dynamic_did(0xF200))
```

### read_dtcs

```python
from pyuds import UDS
uds = UDS()
print(uds.read_dtcs(0x08))
```

### read_dtc_snapshot

```python
from pyuds import UDS
uds = UDS()
print(uds.read_dtc_snapshot("01 23 45"))
```

### read_dtc_extended

```python
from pyuds import UDS
uds = UDS()
print(uds.read_dtc_extended("01 23 45"))
```

### read_supported_dtcs

```python
from pyuds import UDS
uds = UDS()
print(uds.read_supported_dtcs())
```

### clear_dtcs

```python
from pyuds import UDS
uds = UDS()
print(uds.clear_dtcs())
```

### ecu_reset

```python
from pyuds import UDS
uds = UDS()
print(uds.ecu_reset("hard"))
```

### tester_present

```python
from pyuds import UDS
uds = UDS()
print(uds.tester_present())
```

### communication_control

```python
from pyuds import UDS
uds = UDS()
print(uds.communication_control("disable"))
```

### control_dtc_setting

```python
from pyuds import UDS
uds = UDS()
print(uds.control_dtc_setting("off"))
```

### io_control

```python
from pyuds import UDS
uds = UDS()
print(uds.io_control(0x1234, "shortTermAdjustment", "FF"))
```

### routine_control

```python
from pyuds import UDS
uds = UDS()
print(uds.routine_control(0xFF00, "start"))
```

### request_download

```python
from pyuds import UDS
uds = UDS()
print(uds.request_download(0x08000000, 0x10000))
```

### request_upload

```python
from pyuds import UDS
uds = UDS()
print(uds.request_upload(0x08000000, 0x1000))
```

### transfer_data

```python
from pyuds import UDS
uds = UDS()
print(uds.transfer_data(0x01, "AA BB CC"))
```

### request_transfer_exit

```python
from pyuds import UDS
uds = UDS()
print(uds.request_transfer_exit())
```

### request_file_transfer

```python
from pyuds import UDS
uds = UDS()
print(uds.request_file_transfer("add", "/file.bin"))
```

### security_access_seed

```python
from pyuds import UDS
uds = UDS()
print(uds.security_access_seed(level=1))
```

### security_access_key

```python
from pyuds import UDS
uds = UDS()
print(uds.security_access_key(level=1, key_hex="12 34 56 78"))
```

### switch_session

```python
from pyuds import UDS
uds = UDS()
print(uds.switch_session("extended"))
```

### security_access_flow

```python
from pyuds import UDS
uds = UDS()
print(uds.security_access_flow(level=1))
```

### programming_flow

```python
from pyuds import UDS
uds = UDS()
print(uds.programming_flow())
```

### dtc_reading_flow

```python
from pyuds import UDS
uds = UDS()
print(uds.dtc_reading_flow())
```

### io_control_flow

```python
from pyuds import UDS
uds = UDS()
print(uds.io_control_flow(0x1234))
```

### eol_flow

```python
from pyuds import UDS
uds = UDS()
print(uds.eol_flow())
```

### ota_update_flow

```python
from pyuds import UDS
uds = UDS()
print(uds.ota_update_flow())
```

### list_services

```python
from pyuds import UDS
uds = UDS()
print(uds.list_services())
```

### list_dids

```python
from pyuds import UDS
uds = UDS()
print(uds.list_dids())
```

### list_nrcs

```python
from pyuds import UDS
uds = UDS()
print(uds.list_nrcs())
```

### list_routines

```python
from pyuds import UDS
uds = UDS()
print(uds.list_routines())
```

### lookup_nrc

```python
from pyuds import UDS
uds = UDS()
print(uds.lookup_nrc(0x78))
```

### lookup_service

```python
from pyuds import UDS
uds = UDS()
print(uds.lookup_service(0x22))
```

### clear_session

```python
from pyuds import UDS
uds = UDS()
uds.clear_session()
```

### ecu_state

```python
from pyuds import UDS
uds = UDS()
print(uds.ecu_state)
```

## API Docs

::: pyuds.client.UDS
