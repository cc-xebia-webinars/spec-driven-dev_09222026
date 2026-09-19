# Research: Expense Policy Validator

**Phase 0 output** — decisions taken before any design work, with the alternatives
that were considered and why they were set aside.

## Decision: amounts are strings in both data files

**Chosen**: Every monetary value in `policy.json` and in submission files is a quoted
string, parsed into `Decimal` at the boundary.

**Rationale**: Constitution principle IV forbids floats for money. JSON has no decimal
type, so an unquoted `58.00` becomes a float before any of our code sees it, and the
precision is already gone by the time we could object. Quoting moves the conversion
into our control.

**Alternatives considered**: Accepting JSON numbers and converting via `Decimal(str(x))`
was rejected because it hides the problem rather than preventing it — a value like
`0.1 + 0.2` written by a producer would arrive already wrong. The loader now raises
`MalformedInput` on a float, which makes the rule visible to whoever generates the file.

## Decision: exchange rates live in the policy file, keyed by month

**Chosen**: `exchange_rates_to_usd` maps currency to a table of `YYYY-MM` to rate.
Lookup uses the line item's transaction date.

**Rationale**: Clarified on 2026-01-05. Finance publishes a corporate monthly rate, and
using it makes runs deterministic and reproducible — the same submission validated twice
produces the same answer regardless of when it is run.

**Alternatives considered**: Fetching live rates was rejected on two counts. It breaks the
offline constraint, and it makes the tool non-deterministic, which means a dispute cannot
be settled by re-running it. A single fixed corporate rate per year was rejected because
it does not match how Finance actually publishes.

## Decision: proration is a rate in the data file, not a constant

**Chosen**: `partial_day_rate` is `"0.75"` in `policy.json`, applied by `Policy.meal_cap`.

**Rationale**: Constitution principle I. The 75 percent figure is a policy number like any
other and Finance may change it independently of the caps.

**Alternatives considered**: Storing prorated caps directly alongside full caps was
rejected because it duplicates the tier table and lets the two drift apart.

## Decision: the checks return an optional violation rather than raising

**Chosen**: Each `check_*` function returns `Violation | None`. `validate` collects.

**Rationale**: FR-008 requires every violation in one pass. Raising would stop at the
first, which is exactly the behaviour the prompt-built version had and the one Finance
complained about.

**Alternatives considered**: Collecting exceptions in a list was rejected as a misuse of
exceptions for ordinary control flow — a policy violation is an expected outcome, not an
error. `MalformedInput` still raises, because that genuinely is an error and the run
cannot continue.

## Decision: city tier is carried on the submission

**Chosen**: The submission records `city_tier` rather than a destination name.

**Rationale**: Recorded as an assumption in the spec. The tier list changes independently
of this tool, and a name-to-tier mapping would become a second policy table to maintain.

**Alternatives considered**: Deriving the tier from a city name was rejected because it
puts a second source of policy truth inside the validator, which principle I forbids.
