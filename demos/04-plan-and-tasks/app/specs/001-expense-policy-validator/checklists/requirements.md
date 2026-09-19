# Requirements Quality Checklist: Expense Policy Validator

**Purpose**: Validate that the specification is complete, clear and consistent before
planning begins. These are unit tests for the English, not for the code.

**Created by**: `/speckit-specify` · **Re-validated by**: `/speckit-clarify`

**Status after clarification**: 15 of 16 passing (was 12 of 16)

## Requirement Completeness

- [x] CHK001 Every functional requirement states what the system MUST do, not how
- [x] CHK002 No requirement is left with an unresolved `[NEEDS CLARIFICATION]` marker
- [x] CHK003 Each requirement is independently testable without asking a follow-up question
- [x] CHK004 Requirement identifiers are unique and sequential
- [x] CHK005 Every entity referenced by a requirement appears in Key Entities

## Requirement Clarity

- [x] CHK006 Every numeric limit names its unit
- [x] CHK007 Ambiguous words such as "sensibly", "appropriate" and "large" do not appear
- [x] CHK008 Each requirement names the actor that performs the action
- [x] CHK009 Where a default was assumed rather than asked, it is recorded under Assumptions

## Scenario Coverage

- [x] CHK010 Every user story has at least one Given/When/Then acceptance scenario
- [x] CHK011 Each user story is independently testable and independently shippable
- [x] CHK012 Edge cases cover the boundaries the requirements imply
- [ ] CHK013 Every edge case has a corresponding acceptance scenario or test

## Success Criteria

- [x] CHK014 Success criteria are measurable
- [x] CHK015 Success criteria are technology-agnostic
- [x] CHK016 At least one criterion measures the outcome for the people using the tool

---

## Notes

**CHK013 is the one still unchecked, deliberately.** Five edge cases are listed in the
specification and three have direct acceptance scenarios. The single-day trip case and
the negative amount case are covered by tests but not by a scenario in the spec itself.
That is a reviewer's call to make rather than something to auto-fix, which is why the
checklist leaves it visible instead of quietly ticking it.

`/speckit-implement` reads this file and asks before proceeding when items are
unchecked. Deciding what to do about CHK013 is part of the review, not an obstacle
to it.

## What changed during clarification

| Item | Before | After |
|---|---|---|
| CHK002 | Failing — three markers open | Passing — all three resolved |
| CHK003 | Failing — FR-003, FR-004 and FR-006 needed follow-ups | Passing |
| CHK006 | Failing — FR-003 gave no proration figure | Passing — 75 percent stated |
| CHK009 | Passing | Passing — two more assumptions recorded |
