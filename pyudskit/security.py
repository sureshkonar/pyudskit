from __future__ import annotations

from typing import Callable, Dict, Optional


SecurityAlgo = Callable[[bytes, int], bytes]

_ALGORITHMS: Dict[str, SecurityAlgo] = {}


def register_security_algorithm(name: str, func: SecurityAlgo) -> None:
    """Register a SecurityAccess key algorithm by name."""
    _ALGORITHMS[name] = func


def get_security_algorithm(name: str) -> Optional[SecurityAlgo]:
    return _ALGORITHMS.get(name)


def list_security_algorithms() -> list[str]:
    return sorted(_ALGORITHMS.keys())


def compute_key(name: str, seed: bytes, level: int = 1) -> bytes:
    algo = get_security_algorithm(name)
    if algo is None:
        raise ValueError(f"unknown security algorithm: {name}")
    return algo(seed, level)


def _default_algo(seed: bytes, level: int) -> bytes:
    return seed


register_security_algorithm("default", _default_algo)
