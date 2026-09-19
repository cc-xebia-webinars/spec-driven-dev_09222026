# Demo 04 — Plan, Tasks, and a Consistency Check

**Time:** about 14 minutes · **Part of:** on-screen segment 3

The specification says *what* we're building and *why*. This demo is where *how* comes in.
We generate a technical plan and watch it get checked against the constitution, write a
checklist that tests the spec's English, break the plan into ordered tasks, and then run
a consistency pass across everything we've produced.

Four steps run live in the GitHub Copilot chat panel: `/speckit-plan`, `/speckit-checklist`,
`/speckit-tasks` and `/speckit-analyze`.

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
Copilot chat panel and check that the ten commands appear. Leaving `resources/` outside the
workspace is deliberate: our plan and tasks stay out of reach while Copilot writes its own.

**What's already here.** The clarified spec from demo 03 is committed in
`specs/001-expense-policy-validator/spec.md`, along with its quality checklist, and
`.specify/feature.json` points at that folder.

**What you'll produce.** `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, a
`contracts/` folder, a new checklist, and `tasks.md`, all inside the feature folder.

You can confirm the starting state before you begin:

```
uv run python .specify/scripts/python/check_prerequisites.py --json
```

It reports that `plan.md` isn't there yet and suggests running `/speckit-plan`. That's
exactly right. It also shows that Spec Kit has found the feature through `feature.json`.

## What's in this folder

| Path | What it is |
|---|---|
| `app/specs/001-expense-policy-validator/spec.md` | The clarified spec from demo 03 |
| `app/specs/001-expense-policy-validator/checklists/requirements.md` | Its quality checklist |
| `resources/prompts/plan-guidance.md` | What to paste after `/speckit-plan` |
| `resources/prompts/checklist-prompt.md` | What to paste after `/speckit-checklist` |
| `resources/reference/` | Our plan, research, data model, quickstart, contract and tasks |

## Presentation trail

**Step 1 — `specs/001-expense-policy-validator/spec.md`**

Open the spec and scroll to the Clarifications section, so everyone sees where we left
off. Then point out what the spec *doesn't* say: nothing about Python, nothing about
pytest, nothing about file layout. That's deliberate. The spec is written so that Finance
can read and approve it, and technology choices belong somewhere else.

**Step 2 — run `/speckit-plan`**

Type `/speckit-plan` in the chat panel and paste the text from
`resources/prompts/plan-guidance.md`. This is where the technology decisions come in.

This step takes a little while. While it runs, open `resources/reference/plan.md` on the
other half of the screen and walk through it, so the audience sees a complete plan while
the live one is being written.

**Step 3 — `## Technical Context`**

In the plan, find the Technical Context section. It's a list of fields such as
**Language/Version**, **Primary Dependencies** and **Constraints**. Point at Primary
Dependencies, which says there are none at runtime. Hold that thought for the next step.

**Step 4 — `## Constitution Check`**

This is the most important part of the plan. Read the gate line under the heading word
for word:

> *GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Then walk down the table. Each row takes one principle from demo 02 and checks the plan
against it. Principle III says standard library only unless justified, and it passes
because Technical Context said no runtime dependencies. This is where the constitution
stops being a document and starts constraining what gets built.

**Step 5 — `## Complexity Tracking`**

Scroll to the bottom of the plan. There's a table for any principle the plan has to break,
with columns for why it's needed and what simpler option was rejected. Ours is empty.

Explain why that table exists anyway. Sometimes you genuinely need to break a rule, and
when you do, this is where you say so openly, with the reason. It's an honest escape hatch
rather than a hidden one.

**Step 6 — the other plan outputs**

Open the feature folder in the explorer. Next to `plan.md` you'll now see `research.md`,
`data-model.md`, `quickstart.md` and a `contracts/` folder. Open `research.md` briefly:
each decision lists the alternatives that were considered and why they were rejected. Then
open `contracts/cli-contract.md` and point at the exit code table. Exit codes 0, 1 and 2
were decided during clarification in demo 03, and here they are written into a contract
before any code exists.

**Step 7 — run `/speckit-checklist`**

Type `/speckit-checklist` and paste the text from `resources/prompts/checklist-prompt.md`.

Spec Kit's own documentation calls checklists "unit tests for English", and that's a good
way to put it. They don't test code, since none exists yet. They test whether the spec is
precise enough that two people reading it would build the same thing.

When it finishes, look for an item about boundary values. The spec says director approval
is needed above 500 US dollars, but does exactly 500.00 count? A checklist item that asks
that question costs a sentence to resolve now, and a bug report to resolve later.

**Step 8 — run `/speckit-tasks`**

Type `/speckit-tasks` in the chat panel. Like the plan, this takes a moment, so walk
through `resources/reference/tasks.md` while it runs.

**Step 9 — `tasks.md`**

Walk through its structure. Tasks are numbered `T001` onward and grouped into phases:
Setup, then Foundational, then one phase per user story, then Polish. A `[P]` marker means
a task can run in parallel with others, and a story label ties each task back to the user
story it serves.

Point at the Foundational phase heading and its note: these tasks block every user story.
Then find the checkpoint after User Story 1, which says that story can ship on its own.
That's the independence rule from the spec, carried all the way through to the work list.

Scroll to the Notes at the end. The tasks template treats tests as optional by default,
and this project includes them anyway, because constitution principle II requires it. The
constitution has overridden a default, and you can see exactly where.

**Step 10 — run `/speckit-analyze`**

Type `/speckit-analyze`. This reads the spec, the plan and the tasks together and reports
anything that doesn't line up: a requirement with no task, a task with no requirement,
terminology that drifts between documents. It doesn't change any files; it only reports.

If it finds a real inconsistency, let it land. That's the most useful thing that can happen
in this demo. If it comes back clean, you can make the point by editing one `FR-` line in
the spec, running `/speckit-analyze` again, and showing that it notices.

**Step 11 — hand off**

We now have a spec, a plan that passed its constitution check, and an ordered list of
tasks. In the next demo, we hand those tasks to Copilot and let it build.

## If your run differs from ours

Your plan and tasks will be worded differently from ours, and your task numbering may not
match. That's expected. The reference files show one complete, consistent result.

If a step goes wrong, copy our version into place and carry on:

```
cp -r ../resources/reference/. specs/001-expense-policy-validator/
```

## Resetting between runs

From the repository root:

```
git restore demos/04-plan-and-tasks
git clean -fd demos/04-plan-and-tasks
```

That removes everything the live run added to the feature folder and restores the
committed spec, checklist and `feature.json`.
