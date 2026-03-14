# UDS Class

## Method Index

| Category | Methods |
|---|---|
| Beginner | `ask`, `encode`, `decode`, `explain_dtc`, `explain_service`, `explain_session`, `explain_nrc`, `decode_dtc_status`, `parse_dtc_response`, `lookup_did`, `help` |
| Encoding | `encode_request`, `decode_response` |
| Data | `read_did`, `read_dids`, `write_did`, `read_memory`, `write_memory`, `read_scaling_did`, `define_dynamic_did`, `clear_dynamic_did` |
| DTC | `read_dtcs`, `read_dtc_snapshot`, `read_dtc_extended`, `read_supported_dtcs`, `clear_dtcs` |
| Session | `switch_session`, `ecu_reset`, `tester_present`, `communication_control`, `control_dtc_setting` |
| Security | `security_access_seed`, `security_access_key`, `security_access_key_from_seed`, `register_security_algorithm`, `list_security_algorithms` |
| I/O | `io_control` |
| Routine | `routine_control` |
| Flash | `request_download`, `request_upload`, `transfer_data`, `request_transfer_exit`, `request_file_transfer` |
| Flows | `programming_flow`, `security_access_flow`, `dtc_reading_flow`, `io_control_flow`, `eol_flow`, `ota_update_flow` |
| Profiles | `load_profile`, `profile` |
| Utils | `list_services`, `list_dids`, `list_nrcs`, `list_routines`, `lookup_nrc`, `lookup_service`, `export`, `clear_session`, `ecu_state` |

## Examples Per Method

### ask

```python
from pyudskit import UDS
uds = UDS()
print(uds.ask("What is UDS?"))
```

### encode

```python
from pyudskit import UDS
uds = UDS()
print(uds.encode("Read the VIN"))  # 22 F1 90
```

### decode

```python
from pyudskit import UDS
uds = UDS()
print(uds.decode("7F 22 31"))
```

### explain_dtc

```python
from pyudskit import UDS
uds = UDS()
print(uds.explain_dtc("P0301"))
```

### explain_service

```python
from pyudskit import UDS
uds = UDS()
print(uds.explain_service("0x27"))
```

### explain_session

```python
from pyudskit import UDS
uds = UDS()
print(uds.explain_session("programming"))
```

### explain_nrc

```python
from pyudskit import UDS
uds = UDS()
print(uds.explain_nrc("0x22"))
```

### decode_dtc_status

```python
from pyudskit import UDS
uds = UDS()
print(uds.decode_dtc_status(0x2C))
```

### parse_dtc_response

```python
from pyudskit import UDS
uds = UDS()
print(uds.parse_dtc_response("59 02 00 01 02 08"))
```

### lookup_did

```python
from pyudskit import UDS
uds = UDS()
print(uds.lookup_did(0xF190))
```

### help

```python
from pyudskit import UDS
uds = UDS()
uds.help()
```

### encode_request

```python
from pyudskit import UDS
uds = UDS()
print(uds.encode_request("Read the VIN"))
```

### decode_response

```python
from pyudskit import UDS
uds = UDS()
print(uds.decode_response("62 F1 90 57 30 4C 41 53 54"))
```

### read_did

```python
from pyudskit import UDS
uds = UDS()
print(uds.read_did(0xF190))
```

### read_dids

```python
from pyudskit import UDS
uds = UDS()
print(uds.read_dids([0xF190, 0xF186]))
```

### write_did

```python
from pyudskit import UDS
uds = UDS()
print(uds.write_did(0xF190, "31 32 33"))
```

### read_memory

```python
from pyudskit import UDS
uds = UDS()
print(uds.read_memory(0x00001000, 0x10))
```

### write_memory

```python
from pyudskit import UDS
uds = UDS()
print(uds.write_memory(0x00001000, "AA BB"))
```

### read_scaling_did

```python
from pyudskit import UDS
uds = UDS()
print(uds.read_scaling_did(0xF186))
```

### define_dynamic_did

```python
from pyudskit import UDS
uds = UDS()
print(uds.define_dynamic_did(0xF200, [0xF190]))
```

### clear_dynamic_did

```python
from pyudskit import UDS
uds = UDS()
print(uds.clear_dynamic_did(0xF200))
```

### read_dtcs

```python
from pyudskit import UDS
uds = UDS()
print(uds.read_dtcs(0x08))
```

### read_dtc_snapshot

```python
from pyudskit import UDS
uds = UDS()
print(uds.read_dtc_snapshot("01 23 45"))
```

### read_dtc_extended

```python
from pyudskit import UDS
uds = UDS()
print(uds.read_dtc_extended("01 23 45"))
```

### read_supported_dtcs

```python
from pyudskit import UDS
uds = UDS()
print(uds.read_supported_dtcs())
```

### clear_dtcs

```python
from pyudskit import UDS
uds = UDS()
print(uds.clear_dtcs())
```

### ecu_reset

```python
from pyudskit import UDS
uds = UDS()
print(uds.ecu_reset("hard"))
```

### tester_present

```python
from pyudskit import UDS
uds = UDS()
print(uds.tester_present())
```

### communication_control

```python
from pyudskit import UDS
uds = UDS()
print(uds.communication_control("disable"))
```

### control_dtc_setting

```python
from pyudskit import UDS
uds = UDS()
print(uds.control_dtc_setting("off"))
```

### io_control

```python
from pyudskit import UDS
uds = UDS()
print(uds.io_control(0x1234, "shortTermAdjustment", "FF"))
```

### routine_control

```python
from pyudskit import UDS
uds = UDS()
print(uds.routine_control(0xFF00, "start"))
```

### request_download

```python
from pyudskit import UDS
uds = UDS()
print(uds.request_download(0x08000000, 0x10000))
```

### request_upload

```python
from pyudskit import UDS
uds = UDS()
print(uds.request_upload(0x08000000, 0x1000))
```

### transfer_data

```python
from pyudskit import UDS
uds = UDS()
print(uds.transfer_data(0x01, "AA BB CC"))
```

### request_transfer_exit

```python
from pyudskit import UDS
uds = UDS()
print(uds.request_transfer_exit())
```

### request_file_transfer

```python
from pyudskit import UDS
uds = UDS()
print(uds.request_file_transfer("add", "/file.bin"))
```

### security_access_seed

```python
from pyudskit import UDS
uds = UDS()
print(uds.security_access_seed(level=1))
```

### security_access_key

```python
from pyudskit import UDS
uds = UDS()
print(uds.security_access_key(level=1, key_hex="12 34 56 78"))
```

### security_access_key_from_seed

```python
from pyudskit import UDS
uds = UDS()
def algo(seed: bytes, level: int) -> bytes:
    return bytes(b ^ 0xAA for b in seed)
uds.register_security_algorithm("xor", algo)
print(uds.security_access_key_from_seed(1, "A1 B2 C3 D4", "xor"))
```

### register_security_algorithm

```python
from pyudskit import UDS
uds = UDS()
uds.register_security_algorithm("xor", lambda seed, level: bytes(b ^ 0xAA for b in seed))
```

### list_security_algorithms

```python
from pyudskit import UDS
uds = UDS()
print(uds.list_security_algorithms())
```

### switch_session

```python
from pyudskit import UDS
uds = UDS()
print(uds.switch_session("extended"))
```

### security_access_flow

```python
from pyudskit import UDS
uds = UDS()
print(uds.security_access_flow(level=1))
```

### programming_flow

```python
from pyudskit import UDS
uds = UDS()
print(uds.programming_flow())
```

### dtc_reading_flow

```python
from pyudskit import UDS
uds = UDS()
print(uds.dtc_reading_flow())
```

### io_control_flow

```python
from pyudskit import UDS
uds = UDS()
print(uds.io_control_flow(0x1234))
```

### eol_flow

```python
from pyudskit import UDS
uds = UDS()
print(uds.eol_flow())
```

### ota_update_flow

```python
from pyudskit import UDS
uds = UDS()
print(uds.ota_update_flow())
```

### list_services

```python
from pyudskit import UDS
uds = UDS()
print(uds.list_services())
```

### list_dids

```python
from pyudskit import UDS
uds = UDS()
print(uds.list_dids())
```

### list_nrcs

```python
from pyudskit import UDS
uds = UDS()
print(uds.list_nrcs())
```

### list_routines

```python
from pyudskit import UDS
uds = UDS()
print(uds.list_routines())
```

### lookup_nrc

```python
from pyudskit import UDS
uds = UDS()
print(uds.lookup_nrc(0x78))
```

### lookup_service

```python
from pyudskit import UDS
uds = UDS()
print(uds.lookup_service(0x22))
```

### clear_session

```python
from pyudskit import UDS
uds = UDS()
uds.clear_session()
```

### export

```python
from pyudskit import UDS
uds = UDS()
result = uds.read_did(0xF190)
print(uds.export(result, "json"))
```

### ecu_state

```python
from pyudskit import UDS
uds = UDS()
print(uds.ecu_state)
```

### load_profile

```python
from pyudskit import UDS
uds = UDS()
uds.load_profile("pyudskit/profiles/oem_example.json")
```

### profile

```python
from pyudskit import UDS
uds = UDS(profile="pyudskit/profiles/oem_example.json")
print(uds.profile.name)
```

## API Docs

::: pyudskit.client.UDS
