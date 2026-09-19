# Implementation Plan: Expense Policy Validator

**Branch**: `001-expense-policy-validator` | **Date**: 2026-01-05 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-expense-policy-validator/spec.md`

## Summary

Finance needs a command line tool that reads an expense submission and reports every
line that breaks the travel policy, with enough detail to settle a dispute without
reading the source. The approach is a small Python package with no runtime
dependencies: policy values are loaded from a JSON data file, amounts are handled as
decimals throughout, foreign currency is converted using rates carried in that same
data file, and every check runs over every line before anything is reported.

The design follows from two clarified decisions. Conversion happens before cap
comparison, which means currency handling sits underneath the rules rather than
beside them. And every violation is collected rather than returned, which means the
rule functions return an optional violation instead of raising.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: None at runtime. `pytest` for tests only.

**Storage**: Files. A JSON policy file and a JSON submission file, both read-only.

**Testing**: pytest

**Target Platform**: Any desktop or CI environment with Python 3.13. Runs offline.

**Project Type**: Single-package command line tool

**Performance Goals**: A 100-line submission validates in under one second (SC-003).

**Constraints**: No network access, no API keys, no paid services. Exchange rates are
supplied in the policy file rather than fetched, which keeps runs deterministic.

**Scale/Scope**: One submission per run. Roughly 10 functional requirements, 4
entities, 6 modules.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
|---|---|---|
| I. Policy rules live in data, not code | No rule value appears as a literal in application code | PASS — every cap, threshold, tier and rate is read from the policy file by `policy.py` |
| II. Every functional requirement maps to a test | Each `FR-###` has at least one test naming it | PASS — test names carry the requirement id, see `tasks.md` |
| III. Standard library only unless justified | No runtime dependency without a Complexity Tracking entry | PASS — runtime dependencies are empty |
| IV. Money is never a float | All amounts are `Decimal` from the boundary inward | PASS — `money.to_decimal` refuses JSON floats outright |
| V. Report everything, fail predictably | Single pass over all lines, exit codes specified in advance | PASS — FR-008 and FR-009 fix both before implementation |

Re-checked after Phase 1 design: still passing. No entries in Complexity Tracking.

## Project Structure

### Documentation (this feature)

```text
specs/001-expense-policy-validator/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
├── checklists/          # Spec quality checklist and any custom checklists
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
src/expense_validator/
├── __init__.py
├── models.py            # LineItem, ExpenseSubmission, Violation, MalformedInput
├── money.py             # Decimal handling and currency conversion
├── policy.py            # Loading the policy data file, cap and tier lookups
├── rules.py             # Submission parsing and the policy checks
├── report.py            # Text and JSON rendering of a Result
└── cli.py               # Argument parsing and exit codes

tests/
├── conftest.py          # Loads the real policy file, no hand-built fixtures
├── test_money.py        # FR-004, FR-005
├── test_per_diem.py     # FR-002, FR-003
├── test_receipts.py     # FR-006
├── test_approval_tiers.py  # FR-007, SC-002
├── test_currency.py     # FR-004 end to end
└── test_cli.py          # FR-008, FR-009, FR-010, SC-001, SC-004

policy/
├── acme-travel-policy.md   # The human policy document
└── policy.json             # The machine-readable rule data

samples/                 # Five submissions covering the scenarios in the spec
```

**Structure decision**: A single package rather than a library plus a thin CLI. The
tool has one entry point and one consumer, so splitting it would add packaging work
without making anything more testable. `cli.py` stays thin enough that every test
targets the functions underneath it.

## Complexity Tracking

No constitution violations to justify. The table is intentionally empty.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|---|---|---|
| — | — | — |
