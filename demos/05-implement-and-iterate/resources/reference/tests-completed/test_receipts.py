"""The receipt rule.

Covers FR-006 and the acceptance scenarios under User Story 2.
"""

from __future__ import annotations

from decimal import Decimal

from expense_validator.rules import validate


def test_fr006_threshold_comes_from_the_policy_file(policy):
    assert policy.receipt_threshold_usd == Decimal("75.00")


def test_fr006_missing_receipt_above_threshold_is_a_blocking_violation(policy, sample):
    # User Story 2, scenario 1: 120.00 with no receipt. Clarified 2026-01-05 as
    # blocking rather than a warning, so it lands in violations like any other.
    result = validate(sample("receipt-missing"), policy)
    receipts = [v for v in result.violations if v.rule_id == "receipt-required"]
    assert len(receipts) == 1
    assert receipts[0].amount_usd == Decimal("120.00")
    assert receipts[0].limit_usd == Decimal("75.00")
    assert not result.passed


def test_fr006_missing_receipt_below_threshold_is_fine(policy, sample):
    # User Story 2, scenario 2: the 30.00 lunch on the same submission has no
    # receipt and should not be reported.
    result = validate(sample("receipt-missing"), policy)
    reported = {v.line_item.description for v in result.violations if v.line_item}
    assert "Lunch" not in reported


def test_fr006_receipt_present_above_threshold_is_fine(policy, sample):
    # User Story 2, scenario 3. The GBP taxi converts to 57.15 USD which is below
    # the threshold anyway, so use the berlin transport line, which carries R-8821.
    result = validate(sample("berlin-trip"), policy)
    assert [v for v in result.violations if v.rule_id == "receipt-required"] == []


def test_fr006_empty_receipt_string_counts_as_missing(policy, sample):
    submission = sample("receipt-missing")
    item = submission.line_items[0]
    blanked = type(item)(
        date=item.date,
        category=item.category,
        amount=item.amount,
        currency=item.currency,
        receipt="   ",
        description=item.description,
    )
    patched = type(submission)(
        submission_id=submission.submission_id,
        traveller=submission.traveller,
        trip_start=submission.trip_start,
        trip_end=submission.trip_end,
        city_tier=submission.city_tier,
        line_items=[blanked],
    )
    result = validate(patched, policy)
    assert [v for v in result.violations if v.rule_id == "receipt-required"]
