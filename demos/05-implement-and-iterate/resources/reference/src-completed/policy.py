"""Loading the policy data file.

Constitution principle I says policy values live in data, not code. Everything this
module exposes is read from the file - there are no fallback defaults, because a
missing value should be an obvious error rather than a silent assumption.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

from .models import MalformedInput
from .money import to_decimal


def parse_date(value: object, *, what: str) -> date:
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except (TypeError, ValueError) as exc:
        raise MalformedInput(f"{what} is not a date in YYYY-MM-DD form: {value!r}") from exc


@dataclass(frozen=True)
class ApprovalTier:
    id: str
    label: str
    # None means "no upper bound" - the top tier catches everything above the last
    # threshold, so the tier list stays exhaustive without a magic large number.
    max_total_usd: Decimal | None


@dataclass(frozen=True)
class Policy:
    version: str
    meal_caps_usd: dict[str, Decimal]
    partial_day_rate: Decimal
    receipt_threshold_usd: Decimal
    approval_tiers: list[ApprovalTier]
    supported_currencies: list[str]
    exchange_rates_to_usd: dict[str, dict[str, str]]

    @classmethod
    def load(cls, path: str | Path) -> "Policy":
        """Read a policy file. Implements FR-001."""
        p = Path(path)
        try:
            raw = json.loads(p.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise MalformedInput(f"policy file not found: {p}") from exc
        except json.JSONDecodeError as exc:
            raise MalformedInput(f"policy file is not valid JSON: {exc}") from exc

        try:
            caps = {
                str(tier): to_decimal(v, what=f"meal cap for tier {tier}")
                for tier, v in raw["meal_caps_usd"].items()
            }
            tiers = [
                ApprovalTier(
                    id=t["id"],
                    label=t["label"],
                    max_total_usd=(
                        None
                        if t.get("max_total_usd") is None
                        else to_decimal(t["max_total_usd"], what=f"approval tier {t['id']}")
                    ),
                )
                for t in raw["approval_tiers"]
            ]
        except KeyError as exc:
            raise MalformedInput(f"policy file is missing required key: {exc}") from exc

        return cls(
            version=str(raw.get("policy_version", "unknown")),
            meal_caps_usd=caps,
            partial_day_rate=to_decimal(raw["partial_day_rate"], what="partial day rate"),
            receipt_threshold_usd=to_decimal(
                raw["receipt_threshold_usd"], what="receipt threshold"
            ),
            approval_tiers=tiers,
            supported_currencies=list(raw.get("supported_currencies", ["USD"])),
            exchange_rates_to_usd=raw.get("exchange_rates_to_usd", {}),
        )

    def meal_cap(self, city_tier: str, *, partial_day: bool) -> Decimal:
        """The meal cap for a tier, prorated when the day is a partial travel day.

        Implements FR-002 and FR-003. The proration rate comes from the file rather
        than being written as 0.75 here, so that Finance can change it alone.
        """
        if city_tier not in self.meal_caps_usd:
            raise MalformedInput(
                f"city tier {city_tier!r} has no meal cap in the policy file"
            )
        cap = self.meal_caps_usd[city_tier]
        if partial_day:
            cap = (cap * self.partial_day_rate).quantize(Decimal("0.01"))
        return cap

    def approval_tier_for(self, total_usd: Decimal) -> ApprovalTier:
        """The tier a submission total falls into. Implements FR-007."""
        for tier in self.approval_tiers:
            if tier.max_total_usd is None or total_usd <= tier.max_total_usd:
                return tier
        # Only reachable if the file has no open-ended top tier, which load() allows
        # but policy should not do. Better to say so than to return nothing.
        raise MalformedInput(
            "policy file has no approval tier covering a total of "
            f"{total_usd}; the last tier needs a null max_total_usd"
        )
