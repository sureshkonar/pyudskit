from __future__ import annotations

import os
from typing import Optional, Union

from pyudskit.message import UDSMessage
from pyudskit.prompts import (
    SYSTEM_PROMPT,
    ENCODE_PROMPT,
    DECODE_PROMPT,
    DTC_PROMPT,
    SERVICE_PROMPT,
    SESSION_PROMPT,
    NRC_PROMPT,
    FLOW_PROMPT,
)
from pyudskit.registry.dids import COMMON_DIDS
from pyudskit.registry.nrc import UDS_NRC
from pyudskit.registry.routines import COMMON_ROUTINES
from pyudskit.registry.services import UDS_SERVICES
from pyudskit.registry.dtc_status import DTC_STATUS_BITS
from pyudskit.session import UDSSession
from pyudskit.profiles import OEMProfile, load_profile, validate_profile
from pyudskit.utils import (
    bytes_to_hex,
    parse_hex,
    extract_json,
    build_alfid,
    suppress_pos_rsp,
    positive_response_sid,
)


class UDS:
    """
    pyudskit — LLM-powered ISO 14229 UDS assistant.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-20250514",
        verbose: bool = False,
        profile: Optional[Union[str, dict, OEMProfile]] = None,
    ) -> None:
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.verbose = verbose
        self.session = UDSSession()
        self._client = None
        self._profile: Optional[OEMProfile] = None
        if profile is not None:
            self.load_profile(profile)

    def _ensure_client(self) -> None:
        if self._client is not None:
            return
        try:
            from anthropic import Anthropic
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("anthropic package is required") from exc
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set")
        self._client = Anthropic(api_key=self.api_key)

    def _call_llm(self, prompt: str) -> str:
        full_prompt = f"{self.session.context_header()}\n{prompt}"
        self.session.add("user", full_prompt)
        self._ensure_client()
        resp = self._client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": full_prompt}],
        )
        text = ""
        if isinstance(resp, str):
            text = resp
        elif hasattr(resp, "content"):
            parts = resp.content
            if isinstance(parts, list):
                text = "".join(getattr(p, "text", str(p)) for p in parts)
            else:
                text = str(parts)
        else:
            text = str(resp)
        self.session.add("assistant", text)
        if self.verbose:
            print(text)
        return text

    def _build_request(self, data: bytes, service: str, description: str) -> dict:
        msg = UDSMessage.from_bytes(data)
        return {
            "uds_bytes": bytes_to_hex(data),
            "uds_message": msg,
            "service": service,
            "description": description,
        }

    # BEGINNER METHODS
    def ask(self, question: str) -> str:
        return self._call_llm(question)

    def encode(self, description: str) -> str:
        prompt = ENCODE_PROMPT.format(description=description)
        reply = self._call_llm(prompt)
        try:
            data = extract_json(reply)
            return data.get("uds_bytes", "")
        except Exception:
            return reply

    def decode(self, hex_bytes: str) -> str:
        prompt = DECODE_PROMPT.format(hex=hex_bytes)
        reply = self._call_llm(prompt)
        try:
            data = extract_json(reply)
            return data.get("plain_english", "") or data.get("service", "")
        except Exception:
            return reply

    def explain_dtc(self, dtc_code: str) -> str:
        if self._profile and dtc_code in self._profile.dtcs:
            info = self._profile.dtcs[dtc_code]
            name = info.get("name", "OEM DTC")
            desc = info.get("description", "")
            severity = info.get("severity", "")
            parts = [f"{dtc_code} {name}"]
            if desc:
                parts.append(desc)
            if severity:
                parts.append(f"severity: {severity}")
            return " — ".join(parts)
        return self._call_llm(DTC_PROMPT.format(code=dtc_code))

    def explain_service(self, service: str) -> str:
        return self._call_llm(SERVICE_PROMPT.format(service=service))

    def explain_session(self, session: str = "all") -> str:
        return self._call_llm(SESSION_PROMPT.format(session=session))

    def explain_nrc(self, nrc: str) -> str:
        return self._call_llm(NRC_PROMPT.format(nrc=nrc))

    def decode_dtc_status(self, status_byte: int) -> dict[str, bool]:
        return {name: bool(status_byte & bit) for bit, name in DTC_STATUS_BITS.items()}

    def lookup_did(self, did: int) -> str:
        info = None
        if self._profile and did in self._profile.dids:
            info = self._profile.dids[did]
        if not info:
            info = COMMON_DIDS.get(did)
        if not info:
            return "Unknown DID"
        name = info.get("name", "Unknown")
        desc = info.get("description", "")
        return f"0x{did:04X} {name}: {desc}" if desc else f"0x{did:04X} {name}"

    def help(self) -> None:
        print(
            "\n".join(
                [
                    "╔══════════════════════════════════════════════════════════════╗",
                    "║              pyudskit — Quick Reference Guide                   ║",
                    "║         pip install pyudskit  |  from pyudskit import UDS          ║",
                    "╠══════════════════════════════════════════════════════════════╣",
                    "║  BEGINNER                                                    ║",
                    "║  uds.ask(\"What is SecurityAccess?\")   plain English Q&A      ║",
                    "║  uds.encode(\"Read the VIN\")           → \"22 F1 90\"           ║",
                    "║  uds.decode(\"7F 22 31\")               → explanation          ║",
                    "║  uds.explain_dtc(\"P0301\")             → DTC details          ║",
                    "║  uds.explain_service(\"0x27\")          → service deep-dive    ║",
                    "║  uds.explain_session(\"programming\")   → session info         ║",
                    "║  uds.explain_nrc(\"0x22\")              → NRC meaning          ║",
                    "║  uds.decode_dtc_status(0x2C)          → bit flags dict       ║",
                    "║  uds.lookup_did(0xF190)               → DID info             ║",
                    "╠══════════════════════════════════════════════════════════════╣",
                    "║  SERVICE SHORTCUTS                                           ║",
                    "║  uds.read_did(0xF190)                 uds.write_did(...)     ║",
                    "║  uds.read_dtcs(0x08)                  uds.clear_dtcs()       ║",
                    "║  uds.ecu_reset(\"hard\")                uds.tester_present()   ║",
                    "║  uds.switch_session(\"extended\")       uds.routine_control()  ║",
                    "║  uds.io_control(did, \"shortTermAdjustment\", \"FF\")            ║",
                    "║  uds.request_download(addr, size)     uds.transfer_data(...) ║",
                    "╠══════════════════════════════════════════════════════════════╣",
                    "║  FLOWS                                                       ║",
                    "║  uds.programming_flow()               Full flash sequence    ║",
                    "║  uds.security_access_flow(level=1)    Seed-key walkthrough   ║",
                    "║  uds.dtc_reading_flow()               Read + clear DTCs      ║",
                    "║  uds.io_control_flow(did)             I/O control options    ║",
                    "║  uds.eol_flow()                       End-of-line config     ║",
                    "║  uds.ota_update_flow()                OTA update sequence    ║",
                    "╠══════════════════════════════════════════════════════════════╣",
                    "║  UTILITIES                                                   ║",
                    "║  uds.list_services(group=\"DTC Management\")                   ║",
                    "║  uds.list_dids()   uds.list_nrcs()   uds.list_routines()     ║",
                    "║  uds.lookup_nrc(0x78)   uds.ecu_state   uds.clear_session()  ║",
                    "╚══════════════════════════════════════════════════════════════╝",
                ]
            )
        )

    # ADVANCED — Encoding / Decoding
    def encode_request(self, description: str) -> dict:
        prompt = ENCODE_PROMPT.format(description=description)
        reply = self._call_llm(prompt)
        data = extract_json(reply)
        uds_bytes = data.get("uds_bytes", "")
        msg = UDSMessage.from_hex(uds_bytes) if uds_bytes else UDSMessage.from_bytes(b"")
        return {
            "uds_bytes": uds_bytes,
            "uds_message": msg,
            "service": data.get("service", ""),
            "description": data.get("description", ""),
            "raw_reply": reply,
        }

    def decode_response(self, hex_bytes: str) -> dict:
        prompt = DECODE_PROMPT.format(hex=hex_bytes)
        reply = self._call_llm(prompt)
        data = extract_json(reply)
        msg = UDSMessage.from_hex(hex_bytes)
        return {
            "uds_message": msg,
            "service": data.get("service", ""),
            "type": data.get("type", ""),
            "fields": data.get("fields", {}),
            "plain_english": data.get("plain_english", ""),
            "raw_reply": reply,
        }

    # ADVANCED — Service Shortcuts
    def read_did(self, did: int) -> dict:
        data = bytes([0x22, (did >> 8) & 0xFF, did & 0xFF])
        return self._build_request(data, "ReadDataByIdentifier", f"Read DID 0x{did:04X}")

    def read_dids(self, dids: list[int]) -> dict:
        payload = [0x22]
        for did in dids:
            payload.extend([(did >> 8) & 0xFF, did & 0xFF])
        data = bytes(payload)
        return self._build_request(data, "ReadDataByIdentifier", "Read multiple DIDs")

    def write_did(self, did: int, data_hex: str) -> dict:
        data_bytes = parse_hex(data_hex)
        payload = bytes([0x2E, (did >> 8) & 0xFF, did & 0xFF]) + data_bytes
        return self._build_request(payload, "WriteDataByIdentifier", f"Write DID 0x{did:04X}")

    def read_memory(self, address: int, length: int, addr_len: int = 4, size_len: int = 1) -> dict:
        alfid = build_alfid(addr_len, size_len)
        addr_bytes = address.to_bytes(addr_len, "big")
        size_bytes = length.to_bytes(size_len, "big")
        payload = bytes([0x23, alfid]) + addr_bytes + size_bytes
        return self._build_request(payload, "ReadMemoryByAddress", "Read memory by address")

    def write_memory(self, address: int, data_hex: str, addr_len: int = 4) -> dict:
        data_bytes = parse_hex(data_hex)
        alfid = build_alfid(addr_len, 0)
        addr_bytes = address.to_bytes(addr_len, "big")
        payload = bytes([0x3D, alfid]) + addr_bytes + data_bytes
        return self._build_request(payload, "WriteMemoryByAddress", "Write memory by address")

    def read_scaling_did(self, did: int) -> dict:
        payload = bytes([0x24, (did >> 8) & 0xFF, did & 0xFF])
        return self._build_request(payload, "ReadScalingDataByIdentifier", f"Read scaling for DID 0x{did:04X}")

    def define_dynamic_did(self, dynamic_did: int, source_dids: list[int]) -> dict:
        payload = [0x2C, 0x01, (dynamic_did >> 8) & 0xFF, dynamic_did & 0xFF]
        for did in source_dids:
            payload.extend([(did >> 8) & 0xFF, did & 0xFF])
        return self._build_request(bytes(payload), "DynamicallyDefineDataIdentifier", "Define dynamic DID")

    def clear_dynamic_did(self, dynamic_did: int) -> dict:
        payload = bytes([0x2C, 0x03, (dynamic_did >> 8) & 0xFF, dynamic_did & 0xFF])
        return self._build_request(payload, "DynamicallyDefineDataIdentifier", "Clear dynamic DID")

    def read_dtcs(self, status_mask: int = 0x08) -> dict:
        payload = bytes([0x19, 0x02, status_mask])
        return self._build_request(payload, "ReadDTCInformation", "Read DTCs by status mask")

    def read_dtc_snapshot(self, dtc_hex: str, record_num: int = 0xFF) -> dict:
        dtc_bytes = parse_hex(dtc_hex)
        if len(dtc_bytes) != 3:
            raise ValueError("dtc_hex must be 3 bytes")
        payload = bytes([0x19, 0x04]) + dtc_bytes + bytes([record_num])
        return self._build_request(payload, "ReadDTCInformation", "Read DTC snapshot record")

    def read_dtc_extended(self, dtc_hex: str, record_num: int = 0xFF) -> dict:
        dtc_bytes = parse_hex(dtc_hex)
        if len(dtc_bytes) != 3:
            raise ValueError("dtc_hex must be 3 bytes")
        payload = bytes([0x19, 0x06]) + dtc_bytes + bytes([record_num])
        return self._build_request(payload, "ReadDTCInformation", "Read DTC extended data")

    def read_supported_dtcs(self) -> dict:
        payload = bytes([0x19, 0x0A])
        return self._build_request(payload, "ReadDTCInformation", "Read supported DTCs")

    def clear_dtcs(self, group: str = "all") -> dict:
        if group == "all":
            group_bytes = bytes([0xFF, 0xFF, 0xFF])
        else:
            gb = parse_hex(group)
            if len(gb) != 3:
                raise ValueError("group must be 3 bytes or 'all'")
            group_bytes = gb
        payload = bytes([0x14]) + group_bytes
        return self._build_request(payload, "ClearDiagnosticInformation", "Clear DTCs")

    def ecu_reset(self, reset_type: str = "hard") -> dict:
        reset_map = {"hard": 0x01, "keyOffOn": 0x02, "soft": 0x03}
        sub = reset_map.get(reset_type, 0x01)
        payload = bytes([0x11, sub])
        return self._build_request(payload, "ECUReset", f"ECU reset ({reset_type})")

    def tester_present(self, suppress: bool = True) -> dict:
        sub = 0x00
        if suppress:
            sub = suppress_pos_rsp(sub)
        payload = bytes([0x3E, sub])
        self.session.tester_present_active = True
        return self._build_request(payload, "TesterPresent", "Tester present keep-alive")

    def communication_control(self, action: str = "disable") -> dict:
        sub = 0x03 if action == "disable" else 0x00
        payload = bytes([0x28, sub, 0x01])
        self.session.communication_control = "disableRxAndTx" if action == "disable" else "enableRxAndTx"
        return self._build_request(payload, "CommunicationControl", "Communication control")

    def control_dtc_setting(self, setting: str = "off") -> dict:
        sub = 0x02 if setting == "off" else 0x01
        self.session.dtc_setting = "off" if setting == "off" else "on"
        payload = bytes([0x85, sub])
        return self._build_request(payload, "ControlDTCSetting", "Control DTC setting")

    def io_control(self, did: int, option: str, value_hex: str = "") -> dict:
        options = {
            "returnControlToECU": 0x00,
            "resetToDefault": 0x01,
            "freezeCurrentState": 0x02,
            "shortTermAdjustment": 0x03,
        }
        opt = options.get(option, 0x03)
        value_bytes = parse_hex(value_hex) if value_hex else b""
        payload = bytes([0x2F, (did >> 8) & 0xFF, did & 0xFF, opt]) + value_bytes
        return self._build_request(payload, "InputOutputControlByIdentifier", "I/O control")

    def routine_control(self, routine_id: int, action: str = "start", data_hex: str = "") -> dict:
        action_map = {"start": 0x01, "stop": 0x02, "result": 0x03}
        sub = action_map.get(action, 0x01)
        data_bytes = parse_hex(data_hex) if data_hex else b""
        payload = bytes([0x31, sub, (routine_id >> 8) & 0xFF, routine_id & 0xFF]) + data_bytes
        return self._build_request(payload, "RoutineControl", "Routine control")

    def request_download(self, address: int, size: int, compression: int = 0, encrypting: int = 0) -> dict:
        dfi = ((compression & 0x0F) << 4) | (encrypting & 0x0F)
        alfid = build_alfid(4, 4)
        addr_bytes = address.to_bytes(4, "big")
        size_bytes = size.to_bytes(4, "big")
        payload = bytes([0x34, dfi, alfid]) + addr_bytes + size_bytes
        return self._build_request(payload, "RequestDownload", "Request download")

    def request_upload(self, address: int, size: int) -> dict:
        alfid = build_alfid(4, 4)
        addr_bytes = address.to_bytes(4, "big")
        size_bytes = size.to_bytes(4, "big")
        payload = bytes([0x35, 0x00, alfid]) + addr_bytes + size_bytes
        return self._build_request(payload, "RequestUpload", "Request upload")

    def transfer_data(self, block_seq: int, data_hex: str) -> dict:
        data_bytes = parse_hex(data_hex)
        payload = bytes([0x36, block_seq & 0xFF]) + data_bytes
        return self._build_request(payload, "TransferData", "Transfer data block")

    def request_transfer_exit(self) -> dict:
        payload = bytes([0x37])
        return self._build_request(payload, "RequestTransferExit", "Request transfer exit")

    def request_file_transfer(self, mode: str, file_path: str) -> dict:
        mode_map = {"add": 0x01, "delete": 0x02, "replace": 0x03, "read": 0x04}
        mode_byte = mode_map.get(mode, 0x01)
        path_bytes = file_path.encode("ascii", errors="ignore")
        payload = bytes([0x38, mode_byte]) + path_bytes
        return self._build_request(payload, "RequestFileTransfer", "Request file transfer")

    def security_access_seed(self, level: int = 1) -> dict:
        sub = (level * 2) - 1
        payload = bytes([0x27, sub])
        return self._build_request(payload, "SecurityAccess", "Request security seed")

    def security_access_key(self, level: int = 1, key_hex: str = "") -> dict:
        sub = level * 2
        key_bytes = parse_hex(key_hex) if key_hex else b""
        payload = bytes([0x27, sub]) + key_bytes
        return self._build_request(payload, "SecurityAccess", "Send security key")

    def switch_session(self, session: str = "extended") -> dict:
        session_map = {"default": 0x01, "programming": 0x02, "extended": 0x03}
        sub = session_map.get(session, 0x03)
        self.session.set_session(
            "defaultSession" if sub == 0x01 else "programmingSession" if sub == 0x02 else "extendedDiagnosticSession"
        )
        payload = bytes([0x10, sub])
        return self._build_request(payload, "DiagnosticSessionControl", "Switch diagnostic session")

    # ADVANCED — Flows
    def security_access_flow(self, level: int = 1) -> str:
        return self._call_llm(FLOW_PROMPT.format(flow=f"security_access level {level}"))

    def programming_flow(self) -> str:
        return self._call_llm(FLOW_PROMPT.format(flow="programming"))

    def dtc_reading_flow(self) -> str:
        return self._call_llm(FLOW_PROMPT.format(flow="dtc_reading"))

    def io_control_flow(self, did: int) -> str:
        return self._call_llm(FLOW_PROMPT.format(flow=f"io_control for DID 0x{did:04X}"))

    def eol_flow(self) -> str:
        return self._call_llm(FLOW_PROMPT.format(flow="eol"))

    def ota_update_flow(self) -> str:
        return self._call_llm(FLOW_PROMPT.format(flow="ota_update"))

    # UTILITIES
    def list_services(self, group: Optional[str] = None) -> dict[int, str]:
        services = {sid: info["name"] for sid, info in UDS_SERVICES.items()}
        if self._profile:
            for sid, info in self._profile.services.items():
                services[sid] = info.get("name", services.get(sid, "CustomService"))
        if group is None:
            return services
        return {sid: name for sid, name in services.items() if UDS_SERVICES.get(sid, {}).get("group") == group}

    def list_dids(self) -> dict[int, str]:
        dids = {did: info["name"] for did, info in COMMON_DIDS.items()}
        if self._profile:
            for did, info in self._profile.dids.items():
                dids[did] = info.get("name", dids.get(did, "CustomDID"))
        return dids

    def list_nrcs(self) -> dict[int, str]:
        return dict(UDS_NRC)

    def list_routines(self) -> dict[int, str]:
        routines = {rid: info["name"] for rid, info in COMMON_ROUTINES.items()}
        if self._profile:
            for rid, info in self._profile.routines.items():
                routines[rid] = info.get("name", routines.get(rid, "CustomRoutine"))
        return routines

    def lookup_nrc(self, nrc_byte: int) -> str:
        return UDS_NRC.get(nrc_byte, "Unknown NRC")

    def lookup_service(self, sid: int) -> dict:
        info = dict(UDS_SERVICES.get(sid, {}))
        if self._profile and sid in self._profile.services:
            info.update(self._profile.services[sid])
        return info

    def clear_session(self) -> None:
        self.session.reset()

    def load_profile(self, profile: Union[str, dict, OEMProfile]) -> None:
        """
        Load an OEM profile from path, dict, or OEMProfile instance.
        This overrides default services/DIDs/routines/DTCs for lookups.
        """
        if isinstance(profile, OEMProfile):
            self._profile = profile
            return
        if isinstance(profile, str):
            self._profile = load_profile(profile)
            return
        if isinstance(profile, dict):
            validation = validate_profile(profile)
            if not validation.ok:
                raise ValueError("Invalid profile: " + "; ".join(validation.errors))
            self._profile = OEMProfile(
                name=profile.get("name", "custom"),
                dids={int(k, 0): v for k, v in profile.get("dids", {}).items()},
                routines={int(k, 0): v for k, v in profile.get("routines", {}).items()},
                services={int(k, 0): v for k, v in profile.get("services", {}).items()},
                dtcs={str(k): v for k, v in profile.get("dtcs", {}).items()},
            )
            return
        raise TypeError("profile must be a path, dict, or OEMProfile")

    @property
    def profile(self) -> Optional[OEMProfile]:
        return self._profile

    @property
    def ecu_state(self) -> dict:
        return self.session.summary()
