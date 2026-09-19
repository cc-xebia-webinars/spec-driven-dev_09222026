"""Meal per diem caps.

Covers FR-002 and FR-003, and the acceptance scenarios under User Story 1.
"""

from __future__ import annotations

from decimal import Decimal

from expense_validator.rules import validate


def test_fr002_tier_2_full_day_cap_is_sixty_usd(policy):
    assert policy.meal_cap("2", partial_day=False) == Decimal("60.00")


def test_fr002_meal_over_the_tier_cap_is_reported(policy, sample):
    # User Story 1, scenario 1: 72.00 against a 60.00 cap.
    result = validate(sample("over-cap-meal"), policy)
    per_diem = [v for v in result.violations if v.rule_id == "per-diem-cap"]
    assert len(per_diem) == 1
    assert per_diem[0].amount_usd == Decimal("72.00")
    assert per_diem[0].limit_usd == Decimal("60.00")


def test_fr002_meal_under_the_tier_cap_is_not_reported(policy, sample):
    # User Story 1, scenario 2.
    result = validate(sample("berlin-trip"), policy)
    assert [v for v in result.violations if v.rule_id == "per-diem-cap"] == []


def test_fr003_partial_day_cap_is_prorated_to_seventy_five_percent(policy):
    # 60.00 * 0.75 = 45.00
    assert policy.meal_cap("2", partial_day=True) == Decimal("45.00")


def test_fr003_meal_on_a_partial_travel_day_uses_the_prorated_cap(policy, sample):
    # User Story 1, scenario 3: 50.00 on the arrival day is over the 45.00
    # prorated cap, while the identical 50.00 on the full day that follows is not.
    result = validate(sample("partial-travel-day"), policy)
    per_diem = [v for v in result.violations if v.rule_id == "per-diem-cap"]
    assert len(per_diem) == 1
    assert per_diem[0].limit_usd == Decimal("45.00")
    assert str(per_diem[0].line_item.date) == "2026-03-09"


def test_fr003_single_day_trip_prorates_once_not_twice(policy, sample):
    # Edge case from the spec: the one day is both first and last. Proration is a
    # membership test rather than two multiplications, so the cap stays 45.00.
    submission = sample("partial-travel-day")
    one_day = type(submission)(
        submission_id=submission.submission_id,
        traveller=submission.traveller,
        trip_start=submission.trip_start,
        trip_end=submission.trip_start,
        city_tier=submission.city_tier,
        line_items=[submission.line_items[0]],
    )
    result = validate(one_day, policy)
    per_diem = [v for v in result.violations if v.rule_id == "per-diem-cap"]
    assert len(per_diem) == 1
    assert per_diem[0].limit_usd == Decimal("45.00")


def test_fr002_non_meal_categories_are_not_capped(policy, sample):
    # The transport line in this sample is 41.00 and carries a receipt, so it
    # should produce nothing at all.
    result = validate(sample("berlin-trip"), policy)
    assert result.violations == []
