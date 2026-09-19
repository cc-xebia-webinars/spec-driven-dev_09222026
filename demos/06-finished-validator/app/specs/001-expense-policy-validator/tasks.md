# Tasks: Expense Policy Validator

**Input**: Design documents from `/specs/001-expense-policy-validator/`

## Format: `[ID] [P?] [Story] Description`

- **[P]** means the task can run in parallel with others marked `[P]`, because it
  touches files no other parallel task touches.
- **[Story]** names the user story the task belongs to, so a story can be
  implemented and demonstrated on its own.

## Path Conventions

Source lives in `src/expense_validator/`, tests in `tests/`, policy data in
`policy/`, and example submissions in `samples/`.

---

## Phase 1: Setup (Shared Infrastructure)

- [x] T001 Create the package layout `src/expense_validator/` and `tests/`
- [x] T002 Write `pyproject.toml` pinning Python 3.13, declaring no runtime dependencies, and registering the `expense-validate` entry point
- [x] T003 [P] Add `policy/policy.json` with tier caps, proration rate, receipt threshold, approval tiers and monthly exchange rates
- [x] T004 [P] Add the five sample submissions under `samples/` covering the acceptance scenarios

## Phase 2: Foundational (Blocking Prerequisites)

These block every user story, so they come first regardless of priority.

- [x] T005 Define the entities in `src/expense_validator/models.py`: `LineItem`, `ExpenseSubmission`, `Violation`, and the `MalformedInput` error
- [x] T006 Implement decimal handling in `src/expense_validator/money.py`, refusing JSON floats at the boundary (constitution IV)
- [x] T007 Implement currency conversion in `src/expense_validator/money.py` using the rate in force on the transaction date (FR-004, FR-005)
- [x] T008 Implement policy loading in `src/expense_validator/policy.py`, including cap proration and approval tier lookup (FR-001, FR-003, FR-007)

## Phase 3: User Story 1 - Check a submission against the meal per diem (Priority: P1) 🎯 MVP

**Goal**: Report every meal line that exceeds the daily cap for the destination tier,
with partial travel days prorated.

**Independent test**: `uv run pytest tests/test_per_diem.py`

- [x] T009 Implement `check_per_diem` in `src/expense_validator/rules.py` (FR-002, FR-003)
- [x] T010 Implement `check_trip_dates` in `src/expense_validator/rules.py` for the out-of-range edge case
- [x] T011 Implement `validate` in `src/expense_validator/rules.py` so it converts each line to USD, runs every check, and collects all violations in one pass (FR-008)
- [x] T012 [P] Implement text rendering in `src/expense_validator/report.py` so each violation shows its rule id, amount and limit (FR-010, SC-001)
- [x] T013 [P] Implement `src/expense_validator/cli.py` with `--policy`, `--submission` and `--format`, returning exit codes 0, 1 and 2 (FR-009)
- [x] T014 [P] Implement JSON rendering in `src/expense_validator/report.py` for the workflow system
- [x] T015 Verify `tests/test_per_diem.py` passes end to end

**Checkpoint**: User Story 1 is independently shippable here. Finance can check meal
per diem and nothing else, and that alone replaces most of the manual work.

## Phase 4: User Story 2 - Enforce the receipt rule (Priority: P2)

**Goal**: Report line items above the receipt threshold that arrive without a receipt.

**Independent test**: `uv run pytest tests/test_receipts.py`

- [x] T016 Implement `check_receipt` in `src/expense_validator/rules.py` (FR-006)
- [x] T017 Treat a blank or whitespace-only receipt reference as missing
- [x] T018 [P] Add `tests/test_receipts.py` covering the three acceptance scenarios

## Phase 5: User Story 3 - Foreign currency and approval routing (Priority: P3)

**Goal**: Convert EUR and GBP before caps are applied, and report the approval tier.

**Independent test**: `uv run pytest tests/test_currency.py tests/test_approval_tiers.py`

- [x] T019 [P] Add `tests/test_currency.py` asserting conversion happens before the cap comparison
- [x] T020 [P] Add `tests/test_approval_tiers.py` including the boundary case at exactly 500 USD
- [x] T021 Confirm an unsupported currency exits 2 rather than guessing a rate (FR-005)

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T022 [P] Add `tests/test_cli.py` covering all three exit codes and both output formats
- [x] T023 [P] Write `specs/001-expense-policy-validator/quickstart.md`
- [x] T024 Confirm every `FR-###` appears in at least one test name (constitution II)

## Dependencies & Execution Order

Setup blocks Foundational. Foundational blocks all three user stories. The stories
themselves are independent of one another and could be built in any order, though P1
first is what makes an early checkpoint shippable.

Within User Story 1, T009 and T010 can proceed in parallel, T011 depends on both, and
T012 through T014 depend on T011 producing a `Result`.

## Parallel Example: User Story 1

```
T009  check_per_diem      ─┐
T010  check_trip_dates    ─┴─> T011 validate ─┬─> T012 report text
                                              ├─> T013 cli
                                              └─> T014 report json
```

## Implementation Strategy

Build Phase 1 and 2 completely, then stop and run the foundational tests. Those should
be green before any rule is written, because a failure there means the entities or the
money handling are wrong and every later failure would be noise.

Then take User Story 1 to completion and stop again. That checkpoint is a working tool.

## Notes

Tests are included here because the constitution requires every functional requirement
to map to a test. The task template treats tests as optional by default, and this
project overrides that default deliberately.
