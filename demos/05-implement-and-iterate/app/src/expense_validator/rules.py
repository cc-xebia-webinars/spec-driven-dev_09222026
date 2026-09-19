"""The policy checks themselves.

Foundational work is done: this module can already read a submission file and
turn it into the entities the specification describes. The checks are not
written yet - that is tasks T009 through T015, the User Story 1 range, and it is
what the live implementation run in this demo produces.

Do not fill these in by hand. Run the tasks.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from .models import ExpenseSubmission, LineItem, MalformedInput, Violation
from .money import to_decimal
from .policy import ApprovalTier, Policy, parse_date


@dataclass(frozen=True)
class Result:
    """Everything one validation run produced."""

    submission_id: str
    violations: list[Violation]
    total_usd: Decimal
    approval_tier: ApprovalTier

    @property
    def passed(self) -> bool:
        return not self.violations


def load_submission(path: str | Path) -> ExpenseSubmission:
    """Read a submission file, refusing anything we cannot trust.

    T005, complete. Parsing is foundational because every user story needs it.
    """
    p = Path(path)
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise MalformedInput(f"submission file not found: {p}") from exc
    except json.JSONDecodeError as exc:
        raise MalformedInput(f"submission file is not valid JSON: {exc}") from exc

    try:
        items = []
        for i, row in enumerate(raw.get("line_items", []), start=1):
            amount = to_decimal(row["amount"], what=f"line {i} amount")
            if amount < 0:
                raise MalformedInput(f"line {i} has a negative amount: {amount}")
            items.append(
                LineItem(
                    date=parse_date(row["date"], what=f"line {i} date"),
                    category=str(row.get("category", "")),
                    amount=amount,
                    currency=str(row.get("currency", "USD")).upper(),
                    receipt=row.get("receipt"),
                    description=str(row.get("description", "")),
                )
            )
        return ExpenseSubmission(
            submission_id=str(raw["submission_id"]),
            traveller=str(raw.get("traveller", "")),
            trip_start=parse_date(raw["trip_start"], what="trip_start"),
            trip_end=parse_date(raw["trip_end"], what="trip_end"),
            city_tier=str(raw["city_tier"]),
            line_items=items,
        )
    except KeyError as exc:
        raise MalformedInput(f"submission is missing required key: {exc}") from exc


def check_per_diem(
    item: LineItem, usd: Decimal, submission: ExpenseSubmission, policy: Policy
) -> Violation | None:
    """FR-002 and FR-003: meal lines against the daily cap for the tier."""
    raise NotImplementedError("T009: implement the per-diem check (User Story 1)")


def check_receipt(item: LineItem, usd: Decimal, policy: Policy) -> Violation | None:
    """FR-006: a missing receipt above the threshold blocks the submission.

    Not yet enforced. This is task T016, which belongs to User Story 2 and is out of
    scope for this demo's implementation run. It returns None rather than raising so
    that User Story 1 can ship on its own - the spec requires each story to be
    independently shippable, and a story that crashes on another story's unbuilt
    rule isn't. Building User Story 2 replaces this body.
    """
    return None


def check_trip_dates(item: LineItem, submission: ExpenseSubmission) -> Violation | None:
    """Edge case from the spec: a line dated outside the trip is a violation."""
    raise NotImplementedError("T010: implement the trip-date check (User Story 1)")


def validate(submission: ExpenseSubmission, policy: Policy) -> Result:
    """Run every check over every line in one pass.

    FR-008 is why this has to collect rather than return early.
    """
    raise NotImplementedError(
        "T011: implement validate() so it converts each line to USD, runs every "
        "check, and collects all violations in one pass (User Story 1)"
    )
