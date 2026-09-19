# Checklist prompt

Paste this after `/speckit-checklist` in the Copilot chat panel.

---

> Create a checklist for the policy rules. Check that every policy value in the spec
> names its unit, that every rule has a stated limit, that the spec says what happens
> at exactly the boundary value, and that currency handling specifies which rate
> applies and what happens when a rate is missing.

---

## Unit tests for English

The command's own documentation describes checklists as unit tests for English, and
that's a useful way to think about them. They don't test the code, which doesn't exist
yet. They test whether the specification is precise enough that two people reading it
would build the same thing.

The boundary question is the interesting one. The spec says director approval is
needed above 500 USD, but does exactly 500.00 count as above? A checklist item that
asks that question surfaces it now, while it costs a sentence to fix.
