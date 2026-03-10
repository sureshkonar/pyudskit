from __future__ import annotations

import json
from typing import Optional

from pyudskit.message import UDSMessage
from pyudskit.services.base import ServiceResult, UDSService


class PromptBuilder:
    """
    Builds structured prompts from UDS service objects or raw hex.
    """

    @staticmethod
    def build_encode_prompt(description: str, context: dict | None = None) -> str:
        ctx = PromptBuilder.build_context_block(context or {})
        return f"{ctx}\n[TASK]\nEncode this description into UDS bytes.\n[INPUT]\n{description}\n"

    @staticmethod
    def build_decode_prompt(hex_bytes: str, context: dict | None = None) -> str:
        ctx = PromptBuilder.build_context_block(context or {})
        return f"{ctx}\n[TASK]\nDecode this UDS PDU.\n[INPUT]\n{hex_bytes}\n"

    @staticmethod
    def build_service_prompt(service: UDSService, result: ServiceResult) -> str:
        ctx = PromptBuilder.build_context_block({})
        return (
            f"{ctx}\n[TASK]\nExplain and verify this service PDU.\n"
            f"[INPUT]\nService: {service.NAME}\nBuilt bytes: {result.hex_bytes}\nFields: {result.fields}\n"
        )

    @staticmethod
    def build_dtc_prompt(dtc_code: str) -> str:
        return f"[TASK]\nExplain DTC {dtc_code} using SAE J2012 context.\n"

    @staticmethod
    def build_explain_service_prompt(service_name_or_sid: str) -> str:
        return f"[TASK]\nExplain UDS service {service_name_or_sid} in detail.\n"

    @staticmethod
    def build_flow_prompt(flow_name: str, context: dict | None = None) -> str:
        ctx = PromptBuilder.build_context_block(context or {})
        return f"{ctx}\n[TASK]\nProvide a step-by-step flow for {flow_name}.\n"

    @staticmethod
    def build_analyze_prompt(hex_bytes: str) -> str:
        return f"[TASK]\nAnalyze this UDS frame for correctness.\n[INPUT]\n{hex_bytes}\n"

    @staticmethod
    def build_compare_prompt(hex_a: str, hex_b: str) -> str:
        return f"[TASK]\nCompare two UDS frames.\n[INPUT A]\n{hex_a}\n[INPUT B]\n{hex_b}\n"

    @staticmethod
    def inject_output_schema(prompt: str, schema: dict) -> str:
        return f"{prompt}\n[OUTPUT]\nRespond ONLY with valid JSON matching this schema:\n{json.dumps(schema, indent=2)}\n"

    @staticmethod
    def build_context_block(session_state: dict) -> str:
        if not session_state:
            return "[ECU CONTEXT]\nActive Session: unknown\nSecurity Level: unknown\n"
        return (
            "[ECU CONTEXT]\n"
            f"Active Session   : {session_state.get('active_session')}\n"
            f"Security Level   : {session_state.get('security_level')}\n"
            f"DTC Setting      : {session_state.get('dtc_setting')}\n"
            f"Comm Control     : {session_state.get('communication_control')}\n"
        )
