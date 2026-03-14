from __future__ import annotations

from typing import Optional

from pyudskit.client import UDS
from pyudskit.session import UDSSession


class AsyncUDS:
    """Async wrapper around UDS. Uses sync methods under the hood."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514", verbose: bool = False) -> None:
        self._uds = UDS(api_key=api_key, model=model, verbose=verbose)

    @property
    def session(self) -> UDSSession:
        return self._uds.session

    async def ask(self, question: str) -> str:
        return self._uds.ask(question)

    async def encode(self, description: str) -> str:
        return self._uds.encode(description)

    async def decode(self, hex_bytes: str) -> str:
        return self._uds.decode(hex_bytes)

    async def explain_dtc(self, dtc_code: str) -> str:
        return self._uds.explain_dtc(dtc_code)

    async def explain_service(self, service: str) -> str:
        return self._uds.explain_service(service)

    async def explain_session(self, session: str = "all") -> str:
        return self._uds.explain_session(session)

    async def explain_nrc(self, nrc: str) -> str:
        return self._uds.explain_nrc(nrc)

    async def decode_dtc_status(self, status_byte: int) -> dict[str, bool]:
        return self._uds.decode_dtc_status(status_byte)

    async def parse_dtc_response(self, hex_bytes: str) -> dict:
        return self._uds.parse_dtc_response(hex_bytes)

    async def encode_request(self, description: str) -> dict:
        return self._uds.encode_request(description)

    async def decode_response(self, hex_bytes: str) -> dict:
        return self._uds.decode_response(hex_bytes)

    async def read_did(self, did: int) -> dict:
        return self._uds.read_did(did)

    async def read_dids(self, dids: list[int]) -> dict:
        return self._uds.read_dids(dids)

    async def write_did(self, did: int, data_hex: str) -> dict:
        return self._uds.write_did(did, data_hex)

    async def read_memory(self, address: int, length: int, addr_len: int = 4, size_len: int = 1) -> dict:
        return self._uds.read_memory(address, length, addr_len, size_len)

    async def write_memory(self, address: int, data_hex: str, addr_len: int = 4) -> dict:
        return self._uds.write_memory(address, data_hex, addr_len)

    async def read_scaling_did(self, did: int) -> dict:
        return self._uds.read_scaling_did(did)

    async def define_dynamic_did(self, dynamic_did: int, source_dids: list[int]) -> dict:
        return self._uds.define_dynamic_did(dynamic_did, source_dids)

    async def clear_dynamic_did(self, dynamic_did: int) -> dict:
        return self._uds.clear_dynamic_did(dynamic_did)

    async def read_dtcs(self, status_mask: int = 0x08) -> dict:
        return self._uds.read_dtcs(status_mask)

    async def read_dtc_snapshot(self, dtc_hex: str, record_num: int = 0xFF) -> dict:
        return self._uds.read_dtc_snapshot(dtc_hex, record_num)

    async def read_dtc_extended(self, dtc_hex: str, record_num: int = 0xFF) -> dict:
        return self._uds.read_dtc_extended(dtc_hex, record_num)

    async def read_supported_dtcs(self) -> dict:
        return self._uds.read_supported_dtcs()

    async def clear_dtcs(self, group: str = "all") -> dict:
        return self._uds.clear_dtcs(group)

    async def ecu_reset(self, reset_type: str = "hard") -> dict:
        return self._uds.ecu_reset(reset_type)

    async def tester_present(self, suppress: bool = True) -> dict:
        return self._uds.tester_present(suppress)

    async def communication_control(self, action: str = "disable") -> dict:
        return self._uds.communication_control(action)

    async def control_dtc_setting(self, setting: str = "off") -> dict:
        return self._uds.control_dtc_setting(setting)

    async def io_control(self, did: int, option: str, value_hex: str = "") -> dict:
        return self._uds.io_control(did, option, value_hex)

    async def routine_control(self, routine_id: int, action: str = "start", data_hex: str = "") -> dict:
        return self._uds.routine_control(routine_id, action, data_hex)

    async def request_download(self, address: int, size: int, compression: int = 0, encrypting: int = 0) -> dict:
        return self._uds.request_download(address, size, compression, encrypting)

    async def request_upload(self, address: int, size: int) -> dict:
        return self._uds.request_upload(address, size)

    async def transfer_data(self, block_seq: int, data_hex: str) -> dict:
        return self._uds.transfer_data(block_seq, data_hex)

    async def request_transfer_exit(self) -> dict:
        return self._uds.request_transfer_exit()

    async def request_file_transfer(self, mode: str, file_path: str) -> dict:
        return self._uds.request_file_transfer(mode, file_path)

    async def security_access_seed(self, level: int = 1) -> dict:
        return self._uds.security_access_seed(level)

    async def security_access_key(self, level: int = 1, key_hex: str = "") -> dict:
        return self._uds.security_access_key(level, key_hex)

    async def security_access_key_from_seed(self, level: int, seed_hex: str, algorithm: str = "default") -> dict:
        return self._uds.security_access_key_from_seed(level, seed_hex, algorithm)

    async def register_security_algorithm(self, name: str, func) -> None:
        self._uds.register_security_algorithm(name, func)

    async def list_security_algorithms(self) -> list[str]:
        return self._uds.list_security_algorithms()

    async def switch_session(self, session: str = "extended") -> dict:
        return self._uds.switch_session(session)

    async def security_access_flow(self, level: int = 1) -> str:
        return self._uds.security_access_flow(level)

    async def programming_flow(self) -> str:
        return self._uds.programming_flow()

    async def dtc_reading_flow(self) -> str:
        return self._uds.dtc_reading_flow()

    async def io_control_flow(self, did: int) -> str:
        return self._uds.io_control_flow(did)

    async def eol_flow(self) -> str:
        return self._uds.eol_flow()

    async def ota_update_flow(self) -> str:
        return self._uds.ota_update_flow()

    async def list_services(self, group: Optional[str] = None) -> dict[int, str]:
        return self._uds.list_services(group)

    async def list_dids(self) -> dict[int, str]:
        return self._uds.list_dids()

    async def list_nrcs(self) -> dict[int, str]:
        return self._uds.list_nrcs()

    async def list_routines(self) -> dict[int, str]:
        return self._uds.list_routines()

    async def lookup_nrc(self, nrc_byte: int) -> str:
        return self._uds.lookup_nrc(nrc_byte)

    async def lookup_service(self, sid: int) -> dict:
        return self._uds.lookup_service(sid)

    async def clear_session(self) -> None:
        self._uds.clear_session()

    async def export(self, data: dict, fmt: str = "json") -> str:
        return self._uds.export(data, fmt)

    async def load_profile(self, profile) -> None:
        self._uds.load_profile(profile)

    @property
    def profile(self):
        return self._uds.profile

    @property
    def ecu_state(self) -> dict:
        return self._uds.ecu_state
