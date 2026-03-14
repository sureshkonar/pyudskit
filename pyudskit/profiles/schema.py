from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import re


@dataclass
class ProfileValidationResult:
    ok: bool
    errors: list[str] = field(default_factory=list)

_DTC_RE = re.compile(r"^[PCBU][0-9A-F]{4}$")


def _validate_optional_str(obj: dict, key: str, errors: list[str], label: str) -> None:
    if key in obj and not isinstance(obj[key], str):
        errors.append(f"{label}.{key} must be a string")


def _validate_optional_int(obj: dict, key: str, errors: list[str], label: str) -> None:
    if key in obj and not isinstance(obj[key], int):
        errors.append(f"{label}.{key} must be an int")


def _validate_optional_bool(obj: dict, key: str, errors: list[str], label: str) -> None:
    if key in obj and not isinstance(obj[key], bool):
        errors.append(f"{label}.{key} must be a bool")


def _validate_did_entry(key: str, value: dict, errors: list[str]) -> None:
    label = f"DID {key}"
    _validate_optional_str(value, "name", errors, label)
    _validate_optional_str(value, "description", errors, label)
    _validate_optional_str(value, "format", errors, label)
    _validate_optional_str(value, "session_required", errors, label)
    _validate_optional_bool(value, "writable", errors, label)
    if "length_bytes" in value and (not isinstance(value["length_bytes"], int) or value["length_bytes"] <= 0):
        errors.append(f"{label}.length_bytes must be a positive int")
    _validate_optional_int(value, "service", errors, label)


def _validate_routine_entry(key: str, value: dict, errors: list[str]) -> None:
    label = f"Routine {key}"
    _validate_optional_str(value, "name", errors, label)
    _validate_optional_str(value, "description", errors, label)
    _validate_optional_str(value, "session_required", errors, label)


def _validate_service_entry(key: str, value: dict, errors: list[str]) -> None:
    label = f"Service {key}"
    _validate_optional_str(value, "name", errors, label)
    _validate_optional_str(value, "abbr", errors, label)
    _validate_optional_str(value, "group", errors, label)
    _validate_optional_str(value, "description", errors, label)
    _validate_optional_str(value, "request_format", errors, label)
    _validate_optional_str(value, "response_format", errors, label)
    _validate_optional_str(value, "example_request", errors, label)
    _validate_optional_str(value, "example_response", errors, label)
    _validate_optional_int(value, "positive_response_sid", errors, label)
    _validate_optional_int(value, "min_length", errors, label)
    _validate_optional_int(value, "max_length", errors, label)
    if "available_in" in value and not isinstance(value["available_in"], list):
        errors.append(f"{label}.available_in must be a list")
    if "subfunctions" in value and not isinstance(value["subfunctions"], dict):
        errors.append(f"{label}.subfunctions must be a dict")


def _validate_dtc_entry(key: str, value: dict, errors: list[str]) -> None:
    label = f"DTC {key}"
    if not _DTC_RE.match(key.upper()):
        errors.append(f"{label} code format invalid")
    _validate_optional_str(value, "name", errors, label)
    _validate_optional_str(value, "description", errors, label)
    _validate_optional_str(value, "severity", errors, label)

def validate_profile(data: dict) -> ProfileValidationResult:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ProfileValidationResult(False, ["profile must be a dict"])
    if "name" in data and not isinstance(data["name"], str):
        errors.append("name must be a string")
    for key in ("dids", "routines", "services", "dtcs"):
        if key in data and not isinstance(data[key], dict):
            errors.append(f"{key} must be a dict")
    # validate DID entries
    dids = data.get("dids", {})
    for k, v in dids.items():
        try:
            int(k, 0)
        except Exception:
            errors.append(f"invalid DID key: {k}")
        if not isinstance(v, dict):
            errors.append(f"DID {k} must map to object")
            continue
        _validate_did_entry(k, v, errors)
    # validate routines
    routines = data.get("routines", {})
    for k, v in routines.items():
        try:
            int(k, 0)
        except Exception:
            errors.append(f"invalid routine key: {k}")
        if not isinstance(v, dict):
            errors.append(f"Routine {k} must map to object")
            continue
        _validate_routine_entry(k, v, errors)
    # validate services
    services = data.get("services", {})
    for k, v in services.items():
        try:
            int(k, 0)
        except Exception:
            errors.append(f"invalid service key: {k}")
        if not isinstance(v, dict):
            errors.append(f"Service {k} must map to object")
            continue
        _validate_service_entry(k, v, errors)
    # validate DTC catalog
    dtcs = data.get("dtcs", {})
    for k, v in dtcs.items():
        if not isinstance(k, str):
            errors.append("DTC keys must be strings like 'P0301'")
            continue
        if not isinstance(v, dict):
            errors.append(f"DTC {k} must map to object")
            continue
        _validate_dtc_entry(k, v, errors)
    return ProfileValidationResult(len(errors) == 0, errors)
