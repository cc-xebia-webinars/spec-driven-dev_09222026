# Demo 01 — Prompt vs. Spec

**Time:** about 9 minutes · **Part of:** on-screen segment 1

This demo makes the case for spec-driven development before we touch Spec Kit at all.
We'll look at an expense validator that was built from a single, reasonable-sounding
prompt, and then run a set of tests written from the actual travel policy against it.

Nothing here runs an AI tool live. The generated code is already committed, exactly as
it came out, so that everyone sees the same result.

## Before you start

**Tools you'll need**

| Tool | Version | Check with |
|---|---|---|
| `uv` | 0.11 or newer | `uv --version` |
| Python | 3.13 (`uv` installs it for you) | `uv python list` |

That's all for this one. There's no Spec Kit and no Copilot in this demo.

**Setup, from the `app` folder**

```
uv sync
```

## What's in this folder

| Path | What it is |
|---|---|
| `resources/acme-travel-policy.md` | The travel policy, written for people |
| `resources/prompts/one-shot-prompt.md` | The exact prompt that produced the validator |
| `app/src/prompt_built/validator.py` | The validator that prompt produced, unedited |
| `app/tests/test_policy_conformance.py` | Eleven tests written from the policy |
| `app/samples/` | Five example expense submissions |

## Presentation trail

**Step 1 — `resources/acme-travel-policy.md`**

Start with the source of truth. Scroll to section 2 and point at the per-diem table:
the daily meal allowance depends on the city tier, so it's 75, 60 or 45 US dollars
depending on where you travel. Then read section 3 aloud and notice that it talks about
"a threshold" for receipts without ever saying what that threshold is. Section 5 does the
same thing with exchange rates, which it says are converted "at the applicable rate".

This is what real policy documents look like. They're written for people who can ask a
follow-up question, and they leave things out on that assumption.

**Step 2 — `resources/prompts/one-shot-prompt.md`**

Here's the prompt someone wrote to get a validator built. Read it through. It's not a
bad prompt; it mentions the meal allowance, receipts, currencies and approval, which are
all the right topics.

Then scroll down to the table under "What this prompt leaves out". Every row is a
decision the model had to make because the prompt didn't make it. Keep this table open,
because we'll come back to it.

**Step 3 — `app/src/prompt_built/validator.py`**

Now the code that came out. Look at the four constants near the top of the file:
`DAILY_MEAL_CAP`, `RECEIPT_THRESHOLD`, `EXCHANGE_RATES` and `APPROVAL_THRESHOLD`. Each
one has a comment explaining what the prompt said and what the model picked.

The important thing to notice is that every one of these is a *reasonable* guess. Fifty
dollars is a plausible meal allowance. Twenty-five dollars is a plausible receipt
threshold. None of them is right, and nothing in the code tells you that.

Then look at the `validate` function. It returns as soon as it finds the first problem.
The prompt said "tell Finance which lines break policy", and the model read that as one
answer per run.

**Step 4 — run the tests**

```
uv run pytest -v
```

Four tests pass and seven fail. Walk through the passing ones first: a clearly compliant
meal is accepted, an empty submission is accepted, US dollars aren't converted, and a
clean run exits zero. That's the part of the problem a prompt describes well.

Then read the seven failures. Each test name starts with the requirement it checks, such
as `fr002` or `fr006`, and each one lines up with a row in the table from step 2.

**Step 5 — `app/tests/test_policy_conformance.py`**

Open the test file and scroll to the constants at the top: `TIER_CAPS`,
`PARTIAL_DAY_RATE`, `RECEIPT_THRESHOLD` and `EUR_RATE_MARCH`. Read the comment above
them. These values came from asking Finance the questions the policy document left open.

That's the whole argument of this session in one file. The tests aren't smarter than the
model. They simply know things the model was never told, because somebody asked. Spec
Kit gives that asking a place to happen, and a document to record it in, before any code
is written.

**Step 6 — hand off**

Nobody wrote down what was actually wanted, so the model filled in the gaps, and it
filled them in plausibly enough that the result looks finished. In the next demo, we'll
set up Spec Kit and write down the rules that should apply to everything we build.

## If you're following along on your own

This demo is fully deterministic. Your test results will match ours exactly: four
passed, seven failed.

If you want to experiment, try "fixing" the meal cap. Change `DAILY_MEAL_CAP` in
`validator.py` and re-run the three tier tests:

```
uv run pytest -v -k tier
```

Try 75, then 60, then 45. Whichever value you pick, at least one tier test still fails:

| `DAILY_MEAL_CAP` | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| 75.00 | passes | passes | fails |
| 60.00 | fails | passes | fails |
| 45.00 | fails | fails | passes |

There's no number that works, because the policy doesn't have one meal cap. It has three,
chosen by city tier. The model wrote a single constant because the prompt said "the daily
meal allowance", singular, and that one word shaped the design. You can't correct it by
adjusting a value. It needs a different structure, and nobody could know that without
asking.

The same is true of `test_fr008_every_violation_is_reported_not_just_the_first`. It isn't
a wrong number either. The function returns early by design, so no constant will reach it.

Put the original value back when you're done (`DAILY_MEAL_CAP = 50.00`), and the suite
returns to four passed, seven failed.
