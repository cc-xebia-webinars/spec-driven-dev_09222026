# Demo 06 — The Finished Validator and Its Traceability

**Time:** about 4 minutes · **Part of:** on-screen segment 4

This is the finished project: every user story built, every task ticked, every test
passing. We use it to close the loop. Pick any requirement in the spec and you can follow
it to the task that built it, the module where it lives, and the tests that prove it.

Nothing runs an AI tool here. This folder is also the best starting point if you want to
study the complete result after the webinar.

## Before you start

**Tools you'll need**

| Tool | Version | Check with |
|---|---|---|
| `uv` | 0.11 or newer | `uv --version` |
| Python | 3.13 (`uv` installs it for you) | `uv python list` |

**Setup, from the `app` folder**

```
uv sync
```

## What's in this folder

| Path | What it is |
|---|---|
| `app/specs/001-expense-policy-validator/` | The complete design, with every task ticked |
| `app/src/expense_validator/` | The finished validator, six modules |
| `app/tests/` | 38 tests, each named for the requirement it covers |
| `app/policy/policy.json` | Every policy value, as data |
| `app/samples/` | Five example submissions |
| `resources/reference/traceability.md` | Requirement to task to module to test |

## Presentation trail

**Step 1 — run the whole suite**

```
uv run pytest -v
```

Thirty-eight tests, all passing. Scroll through the names. Almost every one begins with a
requirement identifier such as `test_fr003_` or `test_sc004_`, so the list reads like the
spec.

**Step 2 — run every sample**

```
uv run expense-validate --policy policy/policy.json --submission samples/berlin-trip.json
uv run expense-validate --policy policy/policy.json --submission samples/multi-currency.json
```

The first is clean and exits 0. The second is the interesting one: a 58 euro dinner looks
fine against a 60 dollar cap, but converted at the March rate it's 62.64 US dollars, and
that's over. This is why the spec requires conversion to happen before the cap is checked.

**Step 3 — `resources/reference/traceability.md`**

Open the table. Each row is one requirement, with the task that built it, the module it
lives in, and every test that names it.

Tell the audience how this table was made: it's **generated from the test names**, not
written by hand. That's the practical reason constitution principle II asks for the
requirement id in every test name. It turns "is everything tested?" from a judgment call
into a lookup.

Read the line under the table. All ten functional requirements have at least one test.

**Step 4 — the gaps that are meant to be there**

Scroll to the success criteria rows. SC-003 and SC-005 have no tests, and the section
below the table explains why. One is a performance budget and the other is about how many
hours Finance spends each month. Neither is something a unit test can prove, and that's
fine. The functional requirements are the testable contract, while the success criteria
tell you whether the whole effort was worth doing.

> **An honest footnote.** When this table was first generated during preparation for
> this webinar, it flagged FR-001 as having no test naming it, and the test for "report
> every violation" turned out to check only that *at least one* was reported. Both were
> real gaps, and the generated table is what caught them. They're fixed now. It's a small
> example of why making traceability mechanical beats trusting that it's probably fine.

**Step 5 — back to demo 01**
Close by putting two files side by side:
`demos/01-prompt-vs-spec/app/src/prompt_built/validator.py` from demo 01 and
`src/expense_validator/policy.py` here. The first has four hard-coded guesses at the top.
`src/expense_validator/policy.py` here. The first has four hard-coded guesses at the top.
The second has no policy numbers in it at all, because every one comes from
`policy/policy.json`.

Both were written by an AI tool. The difference is that the second one was told what to
build.

## If you're following along on your own

This folder is deterministic. Your results will match ours exactly: 38 passed.

Try constitution principle I for yourself. Open `policy/policy.json`, change
`receipt_threshold_usd` from `"75.00"` to `"100.00"`, and run
`uv run expense-validate --policy policy/policy.json --submission samples/receipt-missing.json`.
The 120 dollar line is still reported, because 120 is over 100, and the message now quotes
the new 100 dollar threshold. You changed behaviour without touching any code.

Then run `uv run pytest`. Three tests fail:

- `test_fr001_every_policy_value_is_read_from_the_file`
- `test_fr006_threshold_comes_from_the_policy_file`
- `test_fr006_missing_receipt_above_threshold_is_a_blocking_violation`

That's the right result. Each of those tests asserts the old 75 dollar value, so together
they're telling you that the data has moved and the spec hasn't. They're also exactly the
tests that the policy-change tasks in demo 05 (T025 to T029) say to update. The failures
aren't a problem to suppress; they're the checklist of what else has to change.

Put the value back to `"75.00"` when you're done, and the suite returns to 38 passed.
