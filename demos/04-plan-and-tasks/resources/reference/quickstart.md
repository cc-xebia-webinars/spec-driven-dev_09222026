# Quickstart: Expense Policy Validator

**Phase 1 output** — how to run the tool once it is built.

## Install

```
uv sync
```

Python 3.13 is pinned in `.python-version` and `uv` installs it if it is missing.
There are no runtime dependencies to resolve.

## Validate a submission

```
uv run expense-validate --policy policy/policy.json --submission samples/berlin-trip.json
```

A clean submission prints the total and the approval tier, then says no violations
were found, and exits 0.

## Read the machine-readable form

```
uv run expense-validate --policy policy/policy.json --submission samples/over-cap-meal.json --format json
```

The JSON output carries the same information plus the rule id, amount and limit for
each violation, which is what the workflow system consumes.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | No violations found |
| 1 | Violations found and reported |
| 2 | Input could not be understood |

These are part of the contract. They were decided during clarification and written
down as FR-009 before any code existed, so a caller can depend on them.

## The samples

| File | Shows |
|---|---|
| `berlin-trip.json` | A clean submission, exit 0 |
| `over-cap-meal.json` | A meal above the tier 2 daily cap |
| `receipt-missing.json` | A 120 USD line above the receipt threshold with no receipt |
| `multi-currency.json` | A EUR line that only breaches the cap after conversion |
| `partial-travel-day.json` | The same amount passing on a full day and failing on a travel day |

The multi-currency sample is the interesting one. The euro figure looks compliant on
its own and only breaches the cap once converted, which is why FR-004 puts conversion
before the comparison.

## Run the tests

```
uv run pytest
```

Every test name carries the requirement it covers, so a failure tells you which part
of the specification stopped holding.

## Change a policy number

Edit `policy/policy.json` and update the test that asserts the old value. No
application code should need to change — that is constitution principle I, and
`test_sc002_changing_a_threshold_needs_no_code_change` checks it.
