# Data Model: Expense Policy Validator

**Phase 1 output** — the entities from the specification, given concrete shapes.

## ExpenseSubmission

One traveller's expenses for one trip.

| Field | Type | Notes |
|---|---|---|
| `submission_id` | str | Finance reference, echoed in every report |
| `traveller` | str | Display only; no lookup is performed |
| `trip_start` | date | First day of travel |
| `trip_end` | date | Last day of travel |
| `city_tier` | str | `"1"`, `"2"` or `"3"`; keys into the cap table |
| `line_items` | list[LineItem] | May be empty |

**Behaviour**: `is_partial_day(day)` returns true when the day is the trip's first or
last. A single-day trip is both, and membership testing makes the prorated cap apply
once rather than twice — the edge case the specification calls out.

## LineItem

A single claimed expense. Immutable once parsed.

| Field | Type | Notes |
|---|---|---|
| `date` | date | Transaction date; also selects the exchange rate period |
| `category` | str | `meal` is the only category the per-diem cap applies to |
| `amount` | Decimal | Always positive; a negative amount is malformed input |
| `currency` | str | `USD`, `EUR` or `GBP`; anything else is malformed input |
| `receipt` | str \| None | Reference, not the document itself |
| `description` | str | Free text from the submitter |

**Behaviour**: `has_receipt` treats an empty or whitespace-only reference as missing,
because submitters send one when a form demands a value they do not have.

## PolicyRule

Not a single class. The policy file carries the rule values and `policy.py` exposes
them through two lookups, which keeps the rule data in one place.

| Rule | Source field | Accessor |
|---|---|---|
| Meal cap by tier | `meal_caps_usd` | `Policy.meal_cap(tier, partial_day=)` |
| Partial day proration | `partial_day_rate` | applied inside `meal_cap` |
| Receipt threshold | `receipt_threshold_usd` | read directly |
| Approval tiers | `approval_tiers` | `Policy.approval_tier_for(total)` |
| Exchange rates | `exchange_rates_to_usd` | `money.convert_to_usd` |

## Violation

One failed check.

| Field | Type | Notes |
|---|---|---|
| `rule_id` | str | `per-diem-cap`, `receipt-required`, `date-outside-trip` |
| `line_item` | LineItem \| None | None for submission-level violations |
| `amount_usd` | Decimal \| None | The converted offending amount |
| `limit_usd` | Decimal \| None | The limit that was exceeded |
| `message` | str | One sentence, written for the submitter |

The rule id and the limit travel with the violation rather than being formatted away,
because SC-001 requires a reviewer to trace any rejection to one named rule.

## Result

What one run produced: the submission id, the list of violations, the USD total, and
the approval tier. `passed` is true when the violation list is empty, which is what the
CLI turns into exit code 0 or 1.

## Relationships

```text
ExpenseSubmission 1 ──── * LineItem
                              │
                              │ checked against
                              ▼
                          Policy (data file)
                              │
                              │ produces
                              ▼
Result 1 ─────────────── * Violation
```
