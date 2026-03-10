from __future__ import annotations

from typing import Optional

import anthropic

from pyudskit.ai.prompt_builder import PromptBuilder
from pyudskit.ai.response_parser import ResponseParser
from pyudskit.ai.schemas import (
    AIEncodeResult,
    AIDecodeResult,
    AIDTCResult,
    AIServiceExplain,
    AIFlowResult,
    AIAnalyzeResult,
)
from pyudskit.prompts import SYSTEM_PROMPT
from pyudskit.services.base import UDSService, ServiceResult
from pyudskit.session import UDSSession


class UDSAIError(RuntimeError):
    pass


class AIClient:
    """
    The LLM AI layer for pyudskit.
    """

    SYSTEM_PROMPT: str = SYSTEM_PROMPT

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-20250514",
        session: Optional[UDSSession] = None,
        verbose: bool = False,
    ) -> None:
        self._client = anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()
        self.model = model
        self.session = session or UDSSession()
        self.verbose = verbose
        self._builder = PromptBuilder()
        self._parser = ResponseParser()

    def _send(self, prompt: str, expect_json: bool = True) -> str:
        full_prompt = f"{self.session.context_header()}\n{prompt}"
        self.session.add("user", full_prompt)
        try:
            resp = self._client.messages.create(
                model=self.model,
                max_tokens=1200,
                system=self.SYSTEM_PROMPT,
                messages=[{"role": "user", "content": full_prompt}],
            )
        except Exception as exc:
            raise UDSAIError(str(exc)) from exc
        text = ""
        if hasattr(resp, "content"):
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

    def _send_json(self, prompt: str) -> dict:
        raw = self._send(prompt, expect_json=True)
        try:
            return self._parser.extract_json(raw)
        except Exception as exc:
            raise UDSAIError("Invalid JSON from LLM") from exc

    def encode(self, description: str) -> AIEncodeResult:
        prompt = self._builder.build_encode_prompt(description, self.session.summary())
        data = self._send_json(prompt)
        return data  # type: ignore[return-value]

    def decode(self, hex_bytes: str) -> AIDecodeResult:
        prompt = self._builder.build_decode_prompt(hex_bytes, self.session.summary())
        data = self._send_json(prompt)
        return data  # type: ignore[return-value]

    def explain_service_result(self, service: UDSService, result: ServiceResult) -> AIDecodeResult:
        prompt = self._builder.build_service_prompt(service, result)
        data = self._send_json(prompt)
        return data  # type: ignore[return-value]

    def verify_service_result(self, service: UDSService, result: ServiceResult) -> AIAnalyzeResult:
        prompt = self._builder.build_service_prompt(service, result)
        data = self._send_json(prompt)
        return data  # type: ignore[return-value]

    def explain_response(self, service: UDSService, response_hex: str) -> AIDecodeResult:
        prompt = self._builder.build_decode_prompt(response_hex, self.session.summary())
        data = self._send_json(prompt)
        return data  # type: ignore[return-value]

    def explain_dtc(self, dtc_code: str) -> AIDTCResult:
        prompt = self._builder.build_dtc_prompt(dtc_code)
        data = self._send_json(prompt)
        return data  # type: ignore[return-value]

    def explain_dtc_status(self, dtc_code: str, status_byte: int) -> str:
        prompt = f"[TASK]\nExplain DTC {dtc_code} with status byte 0x{status_byte:02X}."
        return self._send(prompt, expect_json=False)

    def explain_service(self, service_name_or_sid: str) -> AIServiceExplain:
        prompt = self._builder.build_explain_service_prompt(service_name_or_sid)
        data = self._send_json(prompt)
        return data  # type: ignore[return-value]

    def explain_nrc(self, nrc: str | int) -> str:
        return self._send(f"[TASK]\nExplain NRC {nrc}.", expect_json=False)

    def explain_session(self, session: str) -> str:
        return self._send(f"[TASK]\nExplain UDS session {session}.", expect_json=False)

    def get_flow(self, flow_name: str, **kwargs) -> AIFlowResult:
        prompt = self._builder.build_flow_prompt(flow_name, self.session.summary())
        data = self._send_json(prompt)
        return data  # type: ignore[return-value]

    def analyze(self, hex_bytes: str) -> AIAnalyzeResult:
        prompt = self._builder.build_analyze_prompt(hex_bytes)
        data = self._send_json(prompt)
        return data  # type: ignore[return-value]

    def compare(self, expected_hex: str, actual_hex: str) -> str:
        prompt = self._builder.build_compare_prompt(expected_hex, actual_hex)
        return self._send(prompt, expect_json=False)

    def suggest_next_step(self, last_request: str, last_response: str) -> str:
        prompt = f"[TASK]\nGiven request {last_request} and response {last_response}, suggest next step."
        return self._send(prompt, expect_json=False)

    def chat(self, message: str) -> str:
        return self._send(message, expect_json=False)

    def clear_history(self) -> None:
        self.session.history.clear()

    def reset(self) -> None:
        self.session.reset()
