# Policy Rules Checklist: Expense Policy Validator

**Purpose**: Check that every policy rule in the specification is stated precisely enough
to implement without asking a follow-up question. These test the English, not the code.

**Created by**: `/speckit-checklist` · **Owner**: the reviewer

## Units and Limits

- [x] CHK001 Every monetary limit in the spec names its currency
- [x] CHK002 Every rule states the value of its limit, not just that a limit exists
- [x] CHK003 The proration rule states its rate as a figure (75 percent)
- [x] CHK004 Tier caps are listed for every tier the submission can carry

## Boundary Values

- [ ] CHK005 The spec states whether a total of exactly 500.00 USD needs manager or director approval
- [ ] CHK006 The spec states whether a line of exactly 75.00 USD needs a receipt
- [x] CHK007 The spec states what happens when a trip is a single day

## Currency Handling

- [x] CHK008 The spec names which exchange rate applies, and on which date
- [x] CHK009 The spec says what happens when a currency has no listed rate
- [x] CHK010 The spec says what happens when the rate for a given month is missing

## Consistency

- [x] CHK011 Every rule named in a user story also appears as a functional requirement
- [x] CHK012 Rule values are described as coming from the policy data file, consistent with the constitution

---

## Notes

**CHK005 and CHK006 are the two worth discussing.** The spec says director approval is
needed "above" 500 USD and receipts are needed "above" 75 USD. Most readers take "above"
to mean strictly greater than, so exactly 500.00 stays with the manager and exactly 75.00
needs no receipt. But the spec never says so, and the two readings produce different code.

Finance confirmed the strictly-greater-than reading for both. Resolving that is a one-line
edit to the spec now. Left alone, it would surface as a disagreement between the code and
Finance's expectations after release.

This is why a checklist item that nobody can tick is often more valuable than a dozen that
pass. It points straight at the sentence that needs rewriting.
