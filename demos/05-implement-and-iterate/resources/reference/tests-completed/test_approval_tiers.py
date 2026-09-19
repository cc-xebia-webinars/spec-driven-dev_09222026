"""Approval routing.

Covers FR-007, and SC-002 - the thresholds are data, so changing one should not
require touching application code.
"""

from __future__ import annotations

import json
from decimal import Decimal

from expense_validator.policy import Policy
from expense_validator.rules import validate


def test_fr007_small_total_needs_manager_approval(policy):
    assert policy.approval_tier_for(Decimal("310.00")).id == "manager"


def test_fr007_total_above_five_hundred_needs_director_approval(policy):
    # User Story 3, scenario 3.
    assert policy.approval_tier_for(Decimal("1800.00")).id == "director"


def test_fr007_boundary_total_stays_in_the_lower_tier(policy):
    # Exactly 500.00 is still manager. The tier max is inclusive, which is the
    # reading Finance confirmed.
    assert policy.approval_tier_for(Decimal("500.00")).id == "manager"


def test_fr007_very_large_total_goes_to_finance(policy):
    assert policy.approval_tier_for(Decimal("9000.00")).id == "finance"


def test_fr007_empty_submission_reports_the_lowest_tier(policy, sample):
    # Edge case from the spec: no line items passes with the lowest tier.
    submission = sample("berlin-trip")
    empty = type(submission)(
        submission_id=submission.submission_id,
        traveller=submission.traveller,
        trip_start=submission.trip_start,
        trip_end=submission.trip_end,
        city_tier=submission.city_tier,
        line_items=[],
    )
    result = validate(empty, policy)
    assert result.passed
    assert result.approval_tier.id == "manager"


def test_fr001_every_policy_value_is_read_from_the_file(policy):
    # FR-001 names five kinds of value. Each one has to arrive from the data file,
    # so each one is checked against what policy.json actually says.
    assert policy.meal_caps_usd == {
        "1": Decimal("75.00"), "2": Decimal("60.00"), "3": Decimal("45.00")
    }
    assert policy.partial_day_rate == Decimal("0.75")
    assert policy.receipt_threshold_usd == Decimal("75.00")
    assert [t.id for t in policy.approval_tiers] == ["manager", "director", "finance"]
    assert policy.exchange_rates_to_usd["EUR"]["2026-03"] == "1.08"


def test_sc002_changing_a_threshold_needs_no_code_change(tmp_path, policy_path):
    # The whole point of constitution principle I. Edit the data, get new
    # behaviour, with this module untouched.
    raw = json.loads(policy_path.read_text(encoding="utf-8"))
    raw["approval_tiers"][0]["max_total_usd"] = "100.00"
    edited = tmp_path / "policy.json"
    edited.write_text(json.dumps(raw), encoding="utf-8")

    tightened = Policy.load(edited)
    assert tightened.approval_tier_for(Decimal("310.00")).id == "director"
