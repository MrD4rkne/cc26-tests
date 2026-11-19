"""Shared end-to-end tests for cc26 compilers. See README.md for the contract."""

import os
from dataclasses import dataclass

import pytest


@dataclass(frozen=True)
class Case:
    id: str  # "provider/group/name", stable across runs and xdist workers
    source: str
    stdin: str = ""
    expected: str | None = None  # None -> CPython oracle, computed in the test


def cases() -> list[pytest.ParameterSet]:
    """Cases of the providers named in CT_PROVIDERS (default: DEFAULT)."""
    from cc26_tests.providers import DEFAULT, PROVIDERS

    names = os.environ.get("CT_PROVIDERS", ",".join(DEFAULT)).split(",")
    return [
        pytest.param(c, id=c.id) for n in names if n for c in PROVIDERS[n.strip()]()
    ]
