from typing import TypedDict, Optional


class AIEncodeResult(TypedDict):
    uds_bytes: str
    service: str
    subfunction: Optional[str]
    fields: dict
    description: str
    confidence: str


class AIDecodeResult(TypedDict):
    service: str
    type: str
    subfunction: Optional[str]
    fields: dict
    nrc: Optional[str]
    plain_english: str
    next_step: Optional[str]


class AIDTCResult(TypedDict):
    dtc_code: str
    category: str
    description: str
    root_causes: list[str]
    affected_systems: list[str]
    read_service: str
    clear_service: str
    severity: str


class AIServiceExplain(TypedDict):
    service_name: str
    sid: str
    purpose: str
    request_format: str
    response_format: str
    subfunctions: list[dict]
    session_availability: list[str]
    common_nrcs: list[str]
    example_request: str
    example_response: str


class AIFlowResult(TypedDict):
    flow_name: str
    steps: list[dict]
    total_steps: int
    notes: str


class AIAnalyzeResult(TypedDict):
    service: str
    is_valid: bool
    issues: list[str]
    suggestions: list[str]
    corrected_bytes: Optional[str]
    explanation: str
