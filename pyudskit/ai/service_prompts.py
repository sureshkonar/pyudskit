SERVICE_PROMPTS: dict[str, str] = {
    "DiagnosticSessionControl": """
You are verifying a DiagnosticSessionControl (0x10) request.
Service: {service_name}
Built bytes: {hex_bytes}
Fields: {fields}

Verify:
1. Is the subFunction correct for the requested session?
2. Is this service available in the current session ({active_session})?
3. What is the expected positive response format?
Return JSON only.
""",
    "ECUReset": """
Verify ECUReset (0x11) request.
Service: {service_name}
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "SecurityAccess": """
Verify SecurityAccess (0x27) request.
Built bytes: {hex_bytes}
Fields: {fields}
Include seed/key expectations and NRCs.
Return JSON only.
""",
    "CommunicationControl": """
Verify CommunicationControl (0x28) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "Authentication": """
Verify Authentication (0x29) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "TesterPresent": """
Verify TesterPresent (0x3E) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "AccessTimingParameter": """
Verify AccessTimingParameter (0x83) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "SecuredDataTransmission": """
Verify SecuredDataTransmission (0x84) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "ControlDTCSetting": """
Verify ControlDTCSetting (0x85) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "ResponseOnEvent": """
Verify ResponseOnEvent (0x86) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "LinkControl": """
Verify LinkControl (0x87) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "ReadDataByIdentifier": """
Verify ReadDataByIdentifier (0x22) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "ReadMemoryByAddress": """
Verify ReadMemoryByAddress (0x23) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "ReadScalingDataByIdentifier": """
Verify ReadScalingDataByIdentifier (0x24) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "ReadDataByPeriodicIdentifier": """
Verify ReadDataByPeriodicIdentifier (0x2A) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "DynamicallyDefineDataIdentifier": """
Verify DynamicallyDefineDataIdentifier (0x2C) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "WriteDataByIdentifier": """
Verify WriteDataByIdentifier (0x2E) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "WriteMemoryByAddress": """
Verify WriteMemoryByAddress (0x3D) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "ClearDiagnosticInformation": """
Verify ClearDiagnosticInformation (0x14) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "ReadDTCInformation": """
Verify ReadDTCInformation (0x19) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "InputOutputControlByIdentifier": """
Verify InputOutputControlByIdentifier (0x2F) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "RoutineControl": """
Verify RoutineControl (0x31) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "RequestDownload": """
Verify RequestDownload (0x34) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "RequestUpload": """
Verify RequestUpload (0x35) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "TransferData": """
Verify TransferData (0x36) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "RequestTransferExit": """
Verify RequestTransferExit (0x37) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
    "RequestFileTransfer": """
Verify RequestFileTransfer (0x38) request.
Built bytes: {hex_bytes}
Fields: {fields}
Return JSON only.
""",
}
