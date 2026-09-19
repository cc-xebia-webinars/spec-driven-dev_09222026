"""Shared fixtures.

Everything loads the real policy file rather than a hand-built object, so that the
tests exercise the same path the CLI does and a bad policy file fails the suite.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from expense_validator.policy import Policy
from expense_validator.rules import load_submission

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def policy() -> Policy:
    return Policy.load(ROOT / "policy" / "policy.json")


@pytest.fixture
def sample():
    def _load(name: str):
        return load_submission(ROOT / "samples" / f"{name}.json")

    return _load


@pytest.fixture(scope="session")
def policy_path() -> Path:
    return ROOT / "policy" / "policy.json"


@pytest.fixture(scope="session")
def samples_dir() -> Path:
    return ROOT / "samples"
