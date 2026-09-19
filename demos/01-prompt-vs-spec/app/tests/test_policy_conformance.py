"""Does the prompt-built validator actually follow the travel policy?

These eleven tests were written from the policy after Finance answered the
questions the policy document left open. They are the same answers the
clarification step produces in demo 03, which is the point: somebody had to ask.

Four of these pass. Seven fail. Run `uv run pytest -v` and read the failures
against `src/prompt_built/validator.py`.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from prompt_built import validator  # noqa: E402

# The policy as Finance confirmed it. Every number here is in the real policy or
# was settled by asking. None of them was available to the one-shot prompt.
TIER_CAPS = {"1": 75.00, "2": 60.00, "3": 45.00}
PARTIAL_DAY_RATE = 0.75
RECEIPT_THRESHOLD = 75.00
EUR_RATE_MARCH = 1.08


def submission(items, tier="2", start="2026-03-09", end="2026-03-12"):
    return {
        "submission_id": "TEST",
        "trip_start": start,
        "trip_end": end,
        "city_tier": tier,
        "line_items": items,
    }


def meal(date, amount, currency="USD", receipt="R-1"):
    return {
        "date": date,
        "category": "meal",
        "amount": amount,
        "currency": currency,
        "receipt": receipt,
    }


# ---------------------------------------------------------------- these pass


def test_a_clearly_compliant_meal_is_accepted():
    assert validator.validate(submission([meal("2026-03-10", "20.00")])) is None


def test_a_submission_with_no_lines_is_accepted():
    assert validator.validate(submission([])) is None


def test_usd_amounts_are_not_converted():
    assert validator.convert(42.00, "USD") == 42.00


def test_a_clean_submission_exits_zero(tmp_path):
    import json

    path = tmp_path / "clean.json"
    path.write_text(json.dumps(submission([meal("2026-03-10", "20.00")])), encoding="utf-8")
    assert validator.main([str(path)]) == 0


# ---------------------------------------------------------------- these fail


def test_fr002_tier_1_cap_is_75():
    # Policy section 2. The prompt-built validator uses one flat cap of 50.
    assert validator.DAILY_MEAL_CAP == TIER_CAPS["1"]


def test_fr002_tier_2_cap_is_60():
    result = validator.validate(submission([meal("2026-03-10", "55.00")], tier="2"))
    assert result is None, "55.00 is under the tier 2 cap of 60.00 and should pass"


def test_fr002_tier_3_cap_is_45():
    result = validator.validate(submission([meal("2026-03-10", "47.00")], tier="3"))
    assert result is not None, "47.00 is over the tier 3 cap of 45.00 and should fail"


def test_fr003_first_day_of_a_trip_is_prorated_to_75_percent():
    # 60.00 * 0.75 = 45.00, so a 50.00 meal on the arrival day is over.
    result = validator.validate(submission([meal("2026-03-09", "50.00")]))
    assert result is not None, "50.00 on a partial travel day is over the 45.00 prorated cap"


def test_fr006_receipt_threshold_is_75_not_lower():
    # A 40.00 taxi with no receipt is fine under policy. The prompt-built version
    # flags it, because it guessed the threshold was 25.
    item = {"date": "2026-03-10", "category": "transport", "amount": "40.00",
            "currency": "USD", "receipt": None}
    assert validator.validate(submission([item])) is None


def test_fr004_eur_converts_at_the_published_march_rate():
    assert validator.convert(58.00, "EUR") == round(58.00 * EUR_RATE_MARCH, 2)


def test_fr008_every_violation_is_reported_not_just_the_first():
    # Two separate problems: an over-cap meal and a missing receipt. Policy wants
    # both reported so the analyst can reply once.
    items = [
        meal("2026-03-10", "72.00"),
        {"date": "2026-03-11", "category": "transport", "amount": "120.00",
         "currency": "USD", "receipt": None},
    ]
    result = validator.validate(submission(items))
    assert isinstance(result, list) and len(result) == 2, (
        "expected both violations, got a single value instead"
    )
