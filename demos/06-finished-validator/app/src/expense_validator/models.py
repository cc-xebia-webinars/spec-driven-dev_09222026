"""Data shapes for a submission and the violations found in it.

These mirror the Key Entities section of the specification. They deliberately carry
no validation logic of their own, so that the rules module stays the single place
where policy is applied.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


class MalformedInput(Exception):
    """Raised when a submission or policy file cannot be trusted.

    The CLI turns this into exit code 2. It is deliberately distinct from a policy
    violation: a violation means we understood the submission and it broke a rule,
    while this means we could not understand the submission at all.
    """


@dataclass(frozen=True)
class LineItem:
    """A single claimed expense."""

    date: date
    category: str
    amount: Decimal
    currency: str
    receipt: str | None
    description: str

    @property
    def has_receipt(self) -> bool:
        # An empty string counts as missing. Submitters sometimes send one when the
        # form requires a value but they have nothing to put in it.
        return bool(self.receipt and self.receipt.strip())


@dataclass(frozen=True)
class ExpenseSubmission:
    """One traveller's expenses for one trip."""

    submission_id: str
    traveller: str
    trip_start: date
    trip_end: date
    city_tier: str
    line_items: list[LineItem] = field(default_factory=list)

    def is_partial_day(self, day: date) -> bool:
        """True for the first and last day of the trip.

        A single-day trip is both, which is why this is a membership test rather
        than two separate comparisons. FR-003 requires the prorated cap to be
        applied once in that case, not twice.
        """
        return day in (self.trip_start, self.trip_end)


@dataclass(frozen=True)
class Violation:
    """One failed check, carrying enough detail to settle an argument.

    SC-001 requires that a reviewer can trace any rejection to one named policy
    rule without reading the source, which is why the rule id and the limit travel
    with the violation rather than being formatted away at the point of reporting.
    """

    rule_id: str
    line_item: LineItem | None
    amount_usd: Decimal | None
    limit_usd: Decimal | None
    message: str
