# Change request

This arrives after the validator is built. It's a realistic mid-flight policy change.

---

> Finance has updated the travel policy. From next quarter the receipt threshold
> rises from 75 USD to 100 USD, and we're adding Swiss francs as a supported currency.

---

## How to handle it

The instinct is to open `policy/policy.json`, change 75 to 100, and move on. That
works for the threshold, and constitution principle I is what makes it a one-line
change.

But it leaves the specification saying 75, and within a feature or two the spec stops
describing the system. So instead:

1. Edit `specs/001-expense-policy-validator/spec.md` first. Update FR-006 and the
   User Story 2 scenarios to say 100 USD, and add CHF to FR-004.
2. Run `/speckit-analyze` to see what's now inconsistent across spec, plan and tasks.
3. Run `/speckit-converge` to append the unbuilt work to `tasks.md` as new tasks.

The spec change goes in the same pull request as the code change, and reviewers read
the spec diff first.
