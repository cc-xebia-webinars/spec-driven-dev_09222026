"""Foreign currency end to end.

Covers User Story 3, scenarios 1 and 2, exercising conversion through a real
submission rather than through the conversion helper alone.
"""

from __future__ import annotations

from decimal import Decimal

from expense_validator.rules import validate


def test_fr004_converted_amount_is_compared_against_the_cap(policy, sample):
    # 58.00 EUR at the March rate of 1.08 is 62.64 USD, which is over the 60.00
    # tier 2 cap. The euro figure alone would have looked compliant, which is the
    # whole reason conversion happens before the comparison.
    result = validate(sample("multi-currency"), policy)
    per_diem = [v for v in result.violations if v.rule_id == "per-diem-cap"]
    assert len(per_diem) == 1
    assert per_diem[0].amount_usd == Decimal("62.64")
    assert per_diem[0].limit_usd == Decimal("60.00")


def test_fr004_gbp_line_converts_and_stays_under_the_receipt_threshold(policy, sample):
    # 45.00 GBP at 1.27 is 57.15 USD, below the 75.00 receipt threshold, and it
    # carries a receipt anyway.
    result = validate(sample("multi-currency"), policy)
    assert [v for v in result.violations if v.rule_id == "receipt-required"] == []


def test_fr004_total_is_summed_in_usd_after_conversion(policy, sample):
    # 62.64 + 57.15 = 119.79
    result = validate(sample("multi-currency"), policy)
    assert result.total_usd == Decimal("119.79")
    assert result.approval_tier.id == "manager"
