"""The policy checks themselves.

Every function here takes the policy as an argument rather than reading a module
level constant. That is what makes constitution principle I testable: swap the
policy file and the behaviour changes with no edit to this module.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path

from .models import ExpenseSubmission, LineItem, MalformedInput, Violation
from .money import convert_to_usd, to_decimal
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
    """Read a submission file, refusing anything we cannot trust."""
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
                # Edge case from the spec: a negative claim is not a violation to
                # report, it is a submission we cannot interpret at all.
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
    if item.category != "meal":
        return None
    partial = submission.is_partial_day(item.date)
    cap = policy.meal_cap(submission.city_tier, partial_day=partial)
    if usd <= cap:
        return None
    kind = "prorated partial-day" if partial else "daily"
    return Violation(
        rule_id="per-diem-cap",
        line_item=item,
        amount_usd=usd,
        limit_usd=cap,
        message=(
            f"{item.date} meal of {usd} USD exceeds the {kind} cap of {cap} USD "
            f"for city tier {submission.city_tier}"
        ),
    )


def check_receipt(item: LineItem, usd: Decimal, policy: Policy) -> Violation | None:
    """FR-006: a missing receipt above the threshold blocks the submission."""
    if usd <= policy.receipt_threshold_usd or item.has_receipt:
        return None
    return Violation(
        rule_id="receipt-required",
        line_item=item,
        amount_usd=usd,
        limit_usd=policy.receipt_threshold_usd,
        message=(
            f"{item.date} {item.category} of {usd} USD is above the "
            f"{policy.receipt_threshold_usd} USD receipt threshold and has no receipt"
        ),
    )


def check_trip_dates(item: LineItem, submission: ExpenseSubmission) -> Violation | None:
    """Edge case from the spec: a line dated outside the trip is a violation."""
    if submission.trip_start <= item.date <= submission.trip_end:
        return None
    return Violation(
        rule_id="date-outside-trip",
        line_item=item,
        amount_usd=None,
        limit_usd=None,
        message=(
            f"{item.date} falls outside the trip dates "
            f"{submission.trip_start} to {submission.trip_end}"
        ),
    )


def validate(submission: ExpenseSubmission, policy: Policy) -> Result:
    """Run every check over every line in one pass.

    FR-008 is the reason this collects rather than returns early: an analyst wants
    the whole picture before replying to the submitter, not the first problem.
    """
    violations: list[Violation] = []
    total = Decimal("0.00")

    for item in submission.line_items:
        # Conversion happens before any cap comparison, per FR-004. A currency the
        # policy does not list raises MalformedInput and stops the run - FR-005.
        usd = convert_to_usd(item.amount, item.currency, item.date, policy.exchange_rates_to_usd)
        total += usd

        for found in (
            check_trip_dates(item, submission),
            check_per_diem(item, usd, submission, policy),
            check_receipt(item, usd, policy),
        ):
            if found is not None:
                violations.append(found)

    return Result(
        submission_id=submission.submission_id,
        violations=violations,
        total_usd=total.quantize(Decimal("0.01")),
        approval_tier=policy.approval_tier_for(total),
    )
