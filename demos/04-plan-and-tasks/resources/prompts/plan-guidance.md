# Plan guidance

Paste this after `/speckit-plan` in the Copilot chat panel.

---

> Use Python 3.13 with no runtime dependencies and pytest for tests. This is a single
> package command line tool with an entry point called expense-validate. Store policy
> values in policy/policy.json with amounts as quoted strings. Keep the command line
> layer thin so that tests can target the functions underneath it.

---

## What this adds that the spec deliberately left out

The specification says what the tool does and why. It says nothing about Python,
pytest, or file layout, because those are implementation choices and the spec is meant
to be readable by Finance.

This guidance is where the technology decisions come in, and the plan records them
under Technical Context. Then the Constitution Check reads them back against the
principles from demo 02, which is where you'll see "standard library only" get checked
against "no runtime dependencies".
