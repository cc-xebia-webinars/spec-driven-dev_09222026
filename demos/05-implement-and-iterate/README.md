# Demo 05 — Implement, Then Change the Spec

**Time:** about 14 minutes · **Part of:** on-screen segment 4

Everything up to now has been writing things down. In this demo, GitHub Copilot finally
writes code, working from the task list rather than from a conversation. Then Finance
changes the policy, and we handle it the spec-driven way: by changing the specification
first and letting the tools work out what else needs to change.

Several steps run live in the Copilot chat panel: a scoped `/speckit-implement`, then
`/speckit-analyze` and `/speckit-converge` after the spec changes. The tests run in the
terminal with `uv run pytest`.

## Before you start

**Tools you'll need**

| Tool | Version | Check with |
|---|---|---|
| `uv` | 0.11 or newer | `uv --version` |
| Python | 3.13 (`uv` installs it for you) | `uv python list` |
| Visual Studio Code | current release | `code --version` |
| GitHub Copilot | signed in, with chat enabled | the Copilot icon in the VS Code status bar |
| Git | any recent version | `git --version` |

**Setup, from the `app` folder**

```
uv sync
uv run specify version
code .
```

Open the demo's **`app` folder** as the VS Code workspace, then type `/speckit-` in the
Copilot chat panel and check that the ten commands appear. Our finished source and the
converge output stay in `resources/`, outside the workspace, so Copilot implements the
tasks rather than copying our answers.

**What's already here.** The complete design from demo 04 is committed in
`specs/001-expense-policy-validator/`: spec, plan, research, data model, contract and
tasks. The foundational phase, tasks T001 to T008, is already built and ticked off in
`tasks.md`. That means the data models, the money handling and the policy loading all
exist and work.

**What's missing.** The actual policy checks. That's User Story 1, tasks T009 to T015,
and it's what Copilot builds in this demo.

> **Two test files, two different states, on purpose.** Run `uv run pytest` before you
> start. `tests/test_money.py` passes, because the foundational code is done.
> `tests/test_per_diem.py` fails, because the checks it exercises haven't been written.
> The failure messages name the exact tasks that are missing. That's the state this demo
> starts from, not a broken checkout.

## What's in this folder

| Path | What it is |
|---|---|
| `app/specs/001-expense-policy-validator/` | The full design, with T001–T008 ticked |
| `app/src/expense_validator/` | Foundational code, with the policy checks stubbed out |
| `app/tests/test_money.py` | Passes from a fresh clone |
| `app/tests/test_per_diem.py` | Fails until User Story 1 is implemented |
| `resources/prompts/implement-scope.md` | The scoped implement instruction |
| `resources/prompts/change-request.md` | Finance's mid-flight policy change |
| `resources/reference/src-completed/` | The finished source, for recovery |
| `resources/reference/spec-change.diff` | The spec edit for the policy change |
| `resources/reference/tasks-after-converge.md` | What `/speckit-converge` appends |

## Presentation trail

**Step 1 — run the tests first**

```
uv run pytest
```

Show the split. The money tests pass. Most of the per-diem tests fail, and each failure
message says something like *T011: implement validate()*. Two per-diem tests do pass: the
ones that only check the cap values themselves, which come from the policy file and were
built in the foundational phase. Everything that needs an actual check to run fails.

**Step 2 — `src/expense_validator/rules.py`**

Open the file and scroll through it. `load_submission` is complete, because every user
story needs to read a submission. The three check functions below it are stubs, and each
stub's error message names its task.

Now look at `check_receipt`. It doesn't raise; it just returns `None`, and its docstring
explains why. Checking receipts is User Story 2, which is out of scope today. If it raised
an error, User Story 1 couldn't work without User Story 2 being finished first, and the
spec requires each story to be something you could ship on its own. So a rule from a story
that hasn't been built yet does nothing until that story arrives.

**Step 3 — `specs/001-expense-policy-validator/tasks.md`**

Scroll to Phase 3. Tasks T009 to T015 are unticked. T001 to T008 above them are ticked.
This is the boundary Copilot works within.

**Step 4 — run a scoped `/speckit-implement`**

In the chat panel, type `/speckit-implement` and paste the text from
`resources/prompts/implement-scope.md`. It asks for Phase 3 only, tasks T009 through T015.

Scoping keeps the run to a few minutes. It also shows the real point about staying on
task. Copilot isn't working from a chat history that it might reinterpret. It's working
from a finite, written list, and it can see where that list ends.

Before it starts, `/speckit-implement` checks `checklists/requirements.md`. One item there
is deliberately left unticked (CHK013), so expect it to ask whether you want to go ahead.
Say yes, and mention that this is exactly the kind of gate that stops half-finished specs
from turning into code.

**Step 5 — watch `tasks.md` update**

While Copilot works, keep `tasks.md` open. You'll see T009 onward get ticked as each one is
done. If it starts on User Story 2, point that out, because it means the scope instruction
was ignored rather than the task list being unclear.

**Step 6 — run the tests again**

```
uv run pytest
```

This is the moment the session has been building toward. The per-diem tests now pass, and
their names read like the acceptance scenarios in the spec, because that's where they came
from. Scroll up and point out that `test_fr003_meal_on_a_partial_travel_day_uses_the_prorated_cap`
is exactly the rule the demo 01 validator got wrong.

**Step 7 — run the finished tool**

```
uv run expense-validate --policy policy/policy.json --submission samples/partial-travel-day.json
```

It reports that a 50 US dollar meal on the arrival day exceeds the prorated cap of 45, and
exits with code 1. The same 50 dollars on a full travel day isn't reported.

**Step 8 — the policy changes**

Open `resources/prompts/change-request.md`. Finance is raising the receipt threshold from
75 to 100 US dollars and adding Swiss francs. Talk through the tempting shortcut: open
`policy/policy.json`, change the number, and move on. Constitution principle I is what
makes that a one-line change.

Then explain why we won't do that. The spec would still say 75, and within a feature or two
it would stop describing the system at all.

**Step 9 — edit the spec first**

Open `specs/001-expense-policy-validator/spec.md` and make the change there. Update FR-006
and the User Story 2 scenarios to say 100 US dollars, and add CHF to FR-004. Our version of
the edit is in `resources/reference/spec-change.diff` if you want to follow it exactly.

**Step 10 — run `/speckit-analyze`**

Type `/speckit-analyze`. It now finds that the spec and the tasks disagree: the spec says
100 and CHF, and nothing in `tasks.md` covers either. That's drift, found before anyone
wrote code against a stale requirement.

**Step 11 — run `/speckit-converge`**

Type `/speckit-converge`. It compares the updated spec with the current code and appends
the missing work to `tasks.md` as new tasks. Compare what it adds with
`resources/reference/tasks-after-converge.md`.

Point at the note at the end of that file: **none of the new tasks touch `src/`.** The whole
policy change is data and tests. That's constitution principle I paying off, and it's the
clearest single thing this step shows.

**Step 12 — hand off**

The spec changed first, the tools found everything downstream that needed to follow, and
the code barely had to move. The last demo shows the finished result and how every
requirement traces through to a test.

## If your run differs from ours

Copilot's code won't match ours line for line, and that's fine. What matters is that the
tests pass, because the tests came from the spec.

If the implementation run goes wrong or runs long, copy the finished source into place and
run the same test command:

```
cp ../resources/reference/src-completed/*.py src/expense_validator/
uv run pytest
```

Say plainly that you're doing it and why. The outcome you're demonstrating is the green test
run, and it's the same either way.

## Resetting between runs

From the repository root:

```
git restore demos/05-implement-and-iterate
git clean -fd demos/05-implement-and-iterate
```

That puts the stubs, the unticked tasks and the original spec back, so the per-diem tests
fail again and the demo can be run from the start.
