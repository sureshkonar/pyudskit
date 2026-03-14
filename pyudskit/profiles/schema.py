from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProfileValidationResult:
    ok: bool
    errors: list[str] = field(default_factory=list)


def validate_profile(data: dict) -> ProfileValidationResult:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ProfileValidationResult(False, ["profile must be a dict"])
    if "name" in data and not isinstance(data["name"], str):
        errors.append("name must be a string")
    for key in ("dids", "routines", "services"):
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
    # validate routines
    routines = data.get("routines", {})
    for k, v in routines.items():
        try:
            int(k, 0)
        except Exception:
            errors.append(f"invalid routine key: {k}")
        if not isinstance(v, dict):
            errors.append(f"Routine {k} must map to object")
    # validate services
    services = data.get("services", {})
    for k, v in services.items():
        try:
            int(k, 0)
        except Exception:
            errors.append(f"invalid service key: {k}")
        if not isinstance(v, dict):
            errors.append(f"Service {k} must map to object")
    return ProfileValidationResult(len(errors) == 0, errors)
