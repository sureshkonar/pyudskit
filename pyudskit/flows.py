from pyudskit.prompts import FLOW_PROMPT


FLOW_NAMES = {
    "programming": "programming",
    "security_access": "security_access",
    "dtc_reading": "dtc_reading",
    "io_control": "io_control",
    "eol": "eol",
    "ota_update": "ota_update",
}


def flow_prompt(flow: str) -> str:
    return FLOW_PROMPT.format(flow=flow)
