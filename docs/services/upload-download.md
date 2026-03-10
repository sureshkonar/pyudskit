# Upload & Download Services

## RequestDownload (0x34)

Initiate a download (flash programming) sequence.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x34 | Service identifier |
| 1 | dataFormatIdentifier | byte | Compression/encryption |
| 2 | ALFID | byte | Address/size format |
| 3–N | address + size | bytes | Target region |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x74 | Positive response |
| 1 | lengthFormatIdentifier | byte | Length format |
| 2–N | maxNumberOfBlockLength | bytes | Max block size |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x70 | uploadDownloadNotAccepted |
| 0x31 | requestOutOfRange |

### Subfunctions

None.

### Session Availability

Programming.

### pyuds Example

```python
from pyuds import UDS
uds = UDS()
print(uds.request_download(0x08000000, 0x10000)["uds_bytes"])  # 34 ...
```

!!! warning "Erase first"
    Many ECUs require an erase routine before download.

---

## RequestUpload (0x35)

Initiate an upload (read ECU memory) sequence.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x35 | Service identifier |
| 1 | dataFormatIdentifier | byte | Compression/encryption |
| 2 | ALFID | byte | Address/size format |
| 3–N | address + size | bytes | Target region |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x75 | Positive response |
| 1 | lengthFormatIdentifier | byte | Length format |
| 2–N | maxNumberOfBlockLength | bytes | Max block size |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x70 | uploadDownloadNotAccepted |
| 0x31 | requestOutOfRange |

### Session Availability

Programming, Extended.

### pyuds Example

```python
from pyuds import UDS
uds = UDS()
print(uds.request_upload(0x08000000, 0x1000)["uds_bytes"])  # 35 ...
```

!!! warning "Access control"
    Uploading memory may be restricted by security level.

---

## TransferData (0x36)

Transfer a single data block.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x36 | Service identifier |
| 1 | blockSequenceCounter | byte | Block number |
| 2–N | data | bytes | Payload |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x76 | Positive response |
| 1 | blockSequenceCounter | echo | Echo counter |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x73 | wrongBlockSequenceCounter |
| 0x72 | generalProgrammingFailure |

### Session Availability

Programming.

### pyuds Example

```python
from pyuds import UDS
uds = UDS()
print(uds.transfer_data(0x01, "AA BB CC")["uds_bytes"])  # 36 01 AA BB CC
```

!!! warning "Sequence"
    Block counters must increment correctly or the ECU will reject the transfer.

---

## RequestTransferExit (0x37)

Finalize upload/download transfer.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x37 | Service identifier |
| 1–N | data | bytes | Optional data |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x77 | Positive response |
| 1–N | data | bytes | Optional data |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x72 | generalProgrammingFailure |

### Session Availability

Programming.

### pyuds Example

```python
from pyuds import UDS
uds = UDS()
print(uds.request_transfer_exit()["uds_bytes"])  # 37
```

!!! warning "Finalize"
    Some ECUs verify CRC after transfer exit and may take time.

---

## RequestFileTransfer (0x38)

File-based OTA transfer operations.

### Request Format

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x38 | Service identifier |
| 1 | modeOfOperation | 0x01–0x04 | Add/Delete/Replace/Read |
| 2–N | filePath + data | bytes | File path and data |

### Response Format (Positive)

| Byte | Field | Value | Description |
|---|---|---|---|
| 0 | SID | 0x78 | Positive response |
| 1 | modeOfOperation | echo | Echo of request |
| 2–N | data | bytes | Result data |

### Negative Responses

| NRC | Meaning |
|---|---|
| 0x31 | requestOutOfRange |
| 0x70 | uploadDownloadNotAccepted |

### Subfunctions

| SubFunction | Name |
|---|---|
| 0x01 | addFile |
| 0x02 | deleteFile |
| 0x03 | replaceFile |
| 0x04 | readFile |

### Session Availability

Programming.

### pyuds Example

```python
from pyuds import UDS
uds = UDS()
print(uds.request_file_transfer("add", "/file.bin")["uds_bytes"])  # 38 01 2F 66 69 6C 65 2E 62 69 6E
```

!!! warning "OTA policy"
    OTA operations usually require authentication and OEM backend approval.
