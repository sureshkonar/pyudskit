# ISO 14229 Service Table

| SID | Name | Abbr | Group | Positive SID | Sessions |
|---|---|---|---|---|---|
| 0x10 | DiagnosticSessionControl | DSC | Session Mgmt | 0x50 | All |
| 0x11 | ECUReset | ER | Session Mgmt | 0x51 | All |
| 0x14 | ClearDiagnosticInformation | CDI | DTC Mgmt | 0x54 | Default/Extended |
| 0x19 | ReadDTCInformation | RDI | DTC Mgmt | 0x59 | Default/Extended |
| 0x22 | ReadDataByIdentifier | RDBI | Data | 0x62 | All |
| 0x23 | ReadMemoryByAddress | RMBA | Data | 0x63 | Extended/Programming |
| 0x24 | ReadScalingDataByIdentifier | RSDBI | Data | 0x64 | Default/Extended |
| 0x27 | SecurityAccess | SA | Session Mgmt | 0x67 | Extended/Programming |
| 0x28 | CommunicationControl | CC | Session Mgmt | 0x68 | Extended |
| 0x29 | Authentication | AUTH | Session Mgmt | 0x69 | Extended/Programming |
| 0x2A | ReadDataByPeriodicIdentifier | RDBPI | Data | 0x6A | Default/Extended |
| 0x2C | DynamicallyDefineDataIdentifier | DDDID | Data | 0x6C | Extended |
| 0x2E | WriteDataByIdentifier | WDBI | Data | 0x6E | Extended/Programming |
| 0x2F | InputOutputControlByIdentifier | IOCBI | I/O | 0x6F | Extended |
| 0x31 | RoutineControl | RC | Routine | 0x71 | Extended/Programming |
| 0x34 | RequestDownload | RD | Upload/Download | 0x74 | Programming |
| 0x35 | RequestUpload | RU | Upload/Download | 0x75 | Programming/Extended |
| 0x36 | TransferData | TD | Upload/Download | 0x76 | Programming |
| 0x37 | RequestTransferExit | RTE | Upload/Download | 0x77 | Programming |
| 0x38 | RequestFileTransfer | RFT | Upload/Download | 0x78 | Programming |
| 0x3D | WriteMemoryByAddress | WMBA | Data | 0x7D | Programming |
| 0x3E | TesterPresent | TP | Session Mgmt | 0x7E | All |
| 0x83 | AccessTimingParameter | ATP | Session Mgmt | 0xC3 | Extended |
| 0x84 | SecuredDataTransmission | SDT | Session Mgmt | 0xC4 | Extended/Programming |
| 0x85 | ControlDTCSetting | CDS | Session Mgmt | 0xC5 | Extended |
| 0x86 | ResponseOnEvent | ROE | Session Mgmt | 0xC6 | Extended |
| 0x87 | LinkControl | LC | Session Mgmt | 0xC7 | Extended |
