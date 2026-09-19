"""Currency conversion and decimal handling.

Covers FR-004 and FR-005, plus constitution principle IV.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from expense_validator.models import MalformedInput
from expense_validator.money import convert_to_usd, rate_period, to_decimal


def test_amounts_arrive_as_exact_decimals():
    assert to_decimal("58.00", what="test") == Decimal("58.00")


def test_float_amounts_are_rejected_before_they_lose_precision():
    # Constitution principle IV. By the time a float reaches us the damage is done,
    # so the boundary refuses it rather than quietly converting.
    with pytest.raises(MalformedInput, match="quoted strings"):
        to_decimal(58.00, what="test")


def test_fr004_rate_period_comes_from_the_transaction_date():
    # Clarified 2026-01-05: the rate in force on the transaction date, not the
    # submission date.
    assert rate_period(date(2026, 3, 17)) == "2026-03"
    assert rate_period(date(2026, 4, 1)) == "2026-04"


def test_fr004_usd_passes_through_untouched(policy):
    got = convert_to_usd(
        Decimal("42.00"), "USD", date(2026, 3, 17), policy.exchange_rates_to_usd
    )
    assert got == Decimal("42.00")


def test_fr004_eur_converts_at_the_march_rate(policy):
    # 58.00 EUR at 1.08 = 62.64 USD
    got = convert_to_usd(
        Decimal("58.00"), "EUR", date(2026, 3, 17), policy.exchange_rates_to_usd
    )
    assert got == Decimal("62.64")


def test_fr004_gbp_converts_at_the_march_rate(policy):
    # 45.00 GBP at 1.27 = 57.15 USD
    got = convert_to_usd(
        Decimal("45.00"), "GBP", date(2026, 3, 17), policy.exchange_rates_to_usd
    )
    assert got == Decimal("57.15")


def test_fr005_unlisted_currency_is_malformed_input_not_a_guess(policy):
    with pytest.raises(MalformedInput, match="no rates in the policy file"):
        convert_to_usd(
            Decimal("10.00"), "CHF", date(2026, 3, 17), policy.exchange_rates_to_usd
        )


def test_fr005_missing_rate_period_is_malformed_input(policy):
    # The spec is explicit that we do not fall back to another month.
    with pytest.raises(MalformedInput, match="no EUR rate for 2026-09"):
        convert_to_usd(
            Decimal("10.00"), "EUR", date(2026, 9, 1), policy.exchange_rates_to_usd
        )
