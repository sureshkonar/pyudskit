from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from pyudskit.profiles.schema import validate_profile


@dataclass
class OEMProfile:
    name: str
    dids: dict[int, dict]
    routines: dict[int, dict]
    services: dict[int, dict]


def load_profile(path: str) -> OEMProfile:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    validation = validate_profile(data)
    if not validation.ok:
        raise ValueError("Invalid profile: " + "; ".join(validation.errors))
    return OEMProfile(
        name=data.get("name", "custom"),
        dids={int(k, 0): v for k, v in data.get("dids", {}).items()},
        routines={int(k, 0): v for k, v in data.get("routines", {}).items()},
        services={int(k, 0): v for k, v in data.get("services", {}).items()},
    )
