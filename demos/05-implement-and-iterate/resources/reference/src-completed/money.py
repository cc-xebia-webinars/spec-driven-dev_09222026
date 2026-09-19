"""Currency handling.

Constitution principle IV says money is never a float, so every amount that enters
the system becomes a Decimal at the boundary and stays one until it is reported.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation

from .models import MalformedInput

# Two places, which is what Finance reports in. Rounding happens once, here, at the
# point a converted amount is produced - not at every intermediate comparison.
CENTS = Decimal("0.01")


def to_decimal(value: object, *, what: str) -> Decimal:
    """Convert an incoming JSON value to Decimal, refusing anything ambiguous.

    Amounts arrive as strings in the policy and submission files precisely so that
    they never pass through a float on the way in. A float here would already have
    lost precision before we could object to it.
    """
    if isinstance(value, float):
        raise MalformedInput(
            f"{what} was a JSON number ({value}); amounts must be quoted strings "
            "so they survive as exact decimals"
        )
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise MalformedInput(f"{what} is not a valid amount: {value!r}") from exc


def rate_period(day: date) -> str:
    """The monthly rate key for a date, e.g. 2026-03.

    Clarified in session 2026-01-05: conversion uses the corporate monthly rate in
    force on the transaction date, so the lookup key comes from the line item's own
    date rather than the submission date.
    """
    return f"{day.year:04d}-{day.month:02d}"


def convert_to_usd(
    amount: Decimal,
    currency: str,
    day: date,
    rates: dict[str, dict[str, str]],
) -> Decimal:
    """Convert an amount to US dollars using the rate in force on `day`.

    Implements FR-004. A currency or period the policy does not list is malformed
    input rather than a guess - FR-005 is explicit that we do not invent a rate.
    """
    if currency == "USD":
        return amount.quantize(CENTS)

    if currency not in rates:
        raise MalformedInput(
            f"currency {currency} has no rates in the policy file; "
            "supported currencies are listed there"
        )

    period = rate_period(day)
    table = rates[currency]
    if period not in table:
        raise MalformedInput(
            f"no {currency} rate for {period} in the policy file; "
            "Finance publishes rates monthly and this one is missing"
        )

    rate = to_decimal(table[period], what=f"{currency} rate for {period}")
    return (amount * rate).quantize(CENTS)
