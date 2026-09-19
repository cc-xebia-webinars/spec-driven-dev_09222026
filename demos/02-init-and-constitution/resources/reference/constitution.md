# Expense Policy Validator Constitution

## Core Principles

### I. Policy Rules Live in Data, Not Code

Every reimbursement rule — caps, thresholds, tiers, approval limits — is read from a
policy data file at runtime. No rule value may be written as a literal in application
code. When Finance changes a number, the change is a data edit and a test update, never
a code change. Any pull request that hard-codes a policy value is rejected.

### II. Every Functional Requirement Maps to a Test

Each `FR-###` in the specification has at least one automated test whose name references
that requirement identifier. A requirement with no test is treated as unimplemented,
regardless of what the code does. This is what makes the specification verifiable rather
than aspirational.

### III. Standard Library Only Unless the Plan Justifies Otherwise

The validator runs with no third-party runtime dependencies. Any proposed dependency must
be recorded in the plan's Complexity Tracking table with the simpler alternative that was
rejected and why. Test tooling is exempt from this rule.

### IV. Money Is Never a Float

All monetary values use `decimal.Decimal`. Currency conversion, cap comparison, and
proration are decimal operations throughout. Rounding is applied once, at the point of
reporting, and the rounding rule is stated in the specification rather than left to the
implementation.

### V. Report Everything, Fail Predictably

The validator reports every violation it finds in a single pass rather than stopping at
the first. Exit codes are part of the contract and are specified before implementation:
callers depend on them, so changing one is a breaking change.

## Additional Constraints

The validator runs offline. It reads no network resources, requires no API keys, and
depends on no paid service. Exchange rates are supplied in the policy data file rather
than fetched, which keeps the tool deterministic and testable.

Python version is pinned per project. The supported version is recorded in
`pyproject.toml` and in `.python-version`, and both must agree.

## Development Workflow

Work proceeds specification first. A change to behaviour begins as a change to `spec.md`,
which then flows through planning and task generation before any code is edited. Patching
the code and updating the specification afterwards is the failure mode this project exists
to avoid.

Every pull request includes the specification change alongside the code change. Reviewers
read the specification diff first.

## Governance

This constitution takes precedence over convenience. The Constitution Check gate in
`plan.md` must pass before research begins and must be rechecked after design. Violations
are not silently permitted; they are recorded in the plan's Complexity Tracking table with
the justification and the rejected alternative, so that the cost is visible.

Amendments require a version bump here and a note in the plan that depends on them.

**Version**: 1.0.0 | **Ratified**: 2026-01-05 | **Last Amended**: 2026-01-05
