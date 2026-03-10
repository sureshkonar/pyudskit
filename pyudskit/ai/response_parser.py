from __future__ import annotations

import json
import re
from typing import Any

from pyudskit.ai.schemas import (
    AIEncodeResult,
    AIDecodeResult,
    AIDTCResult,
    AIServiceExplain,
    AIFlowResult,
    AIAnalyzeResult,
)


class ResponseParseError(ValueError):
    pass


class ResponseParser:
    """
    Parses raw LLM text responses into typed dicts.
    """

    def parse_encode(self, raw: str) -> AIEncodeResult:
        data = self.extract_json(raw)
        return data  # type: ignore[return-value]

    def parse_decode(self, raw: str) -> AIDecodeResult:
        data = self.extract_json(raw)
        return data  # type: ignore[return-value]

    def parse_dtc(self, raw: str) -> AIDTCResult:
        data = self.extract_json(raw)
        return data  # type: ignore[return-value]

    def parse_service_explain(self, raw: str) -> AIServiceExplain:
        data = self.extract_json(raw)
        return data  # type: ignore[return-value]

    def parse_flow(self, raw: str) -> AIFlowResult:
        data = self.extract_json(raw)
        return data  # type: ignore[return-value]

    def parse_analyze(self, raw: str) -> AIAnalyzeResult:
        data = self.extract_json(raw)
        return data  # type: ignore[return-value]

    @staticmethod
    def extract_json(text: str) -> dict:
        try:
            return json.loads(text)
        except Exception:
            pass
        fenced = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
        if fenced:
            return json.loads(fenced.group(1))
        start = text.find("{")
        if start == -1:
            raise ResponseParseError("no JSON found")
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(text[start : i + 1])
        raise ResponseParseError("no complete JSON found")

    @staticmethod
    def safe_get(d: dict, key: str, default=None):
        return d.get(key, default)
