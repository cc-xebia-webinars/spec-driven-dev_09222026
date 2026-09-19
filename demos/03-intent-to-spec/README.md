# Demo 03 — From Intent to a Reviewable Spec

**Time:** about 16 minutes · **Part of:** on-screen segment 2

This is the heart of the session. We take a real feature request from Finance, the kind
that arrives in a ticket, and turn it into a specification that someone can review. Along
the way we'll see Spec Kit refuse to guess, and then we'll answer its questions on camera.

Two steps run live: `/speckit-specify` and `/speckit-clarify`, both in the GitHub Copilot
chat panel.

## Before you start

**Tools you'll need**

| Tool | Version | Check with |
|---|---|---|
| `uv` | 0.11 or newer | `uv --version` |
| Python | 3.13 (`uv` installs it for you) | `uv python list` |
| Visual Studio Code | current release | `code --version` |
| GitHub Copilot | signed in, with chat enabled | the Copilot icon in the VS Code status bar |
| Git | any recent version | `git --version` |

Spec Kit is pinned in `pyproject.toml` and comes down with `uv sync`.

**Setup, from the `app` folder**

```
uv sync
uv run specify version
code .
```

Open the demo's **`app` folder** as the VS Code workspace, not the demo folder above it and
not the repository root. Copilot finds the Spec Kit commands in `.github/skills/` relative
to the workspace, so opening a parent folder hides them. Keeping the workspace on `app/`
also keeps `resources/` out of reach, so Copilot writes the spec rather than finding ours.
In the chat panel, type `/speckit-` and check that the ten commands appear.

**What's already here.** The constitution from demo 02 is in `.specify/memory/constitution.md`.
The `specs/` folder is empty. Nothing about this feature has been written yet.

**What you'll produce.** A new `specs/001-expense-policy-validator/` folder containing
`spec.md` and `checklists/requirements.md`.

## What's in this folder

| Path | What it is |
|---|---|
| `resources/acme-travel-policy.md` | The travel policy |
| `resources/prompts/feature-request.md` | The raw request from Finance |
| `resources/prompts/clarify-answers.md` | The answers to give during clarification |
| `app/.specify/memory/constitution.md` | The constitution from demo 02 |
| `app/.github/skills/` | The ten Spec Kit commands |
| `resources/reference/spec.draft.md` | Our spec as `/speckit-specify` produced it |
| `resources/reference/spec.clarified.md` | Our spec after clarification |
| `resources/reference/checklists-requirements.md` | Our quality checklist after clarification |

## Presentation trail

**Step 1 — `resources/acme-travel-policy.md`**

Open the policy and remind everyone of the gaps from demo 01. Section 3 mentions a
receipt threshold without stating it. Section 5 converts currency "at the applicable
rate" without saying which one. Section 2 mentions a reduced rate for partial travel days
without saying what it is. Hold on to these three, because the spec is going to find them.

**Step 2 — `resources/prompts/feature-request.md`**

This is what Finance actually sent. Read it aloud. It's five sentences of honest intent,
and it's more detailed than the one-shot prompt in demo 01, but it still doesn't say what
the caps are, whether they apply per day or per trip, or which exchange rate to use.

That's normal. Requests are written by people who know the domain and assume you do too.

The file ends with one extra line, asking for the short name `expense-policy-validator`.
That line isn't from Finance. It fixes the name of the feature folder so the paths in this
README match, and step 5 checks that it worked.

**Step 3 — `.specify/memory/constitution.md`**

Scroll through the five principles. Point at two in particular: principle I, which says
policy values live in data rather than code, and principle II, which says every functional
requirement maps to a test. `/speckit-specify` reads this file before writing anything, so
these rules are already in force.

**Step 4 — run `/speckit-specify`**

In the Copilot chat panel, type `/speckit-specify` and paste the feature request.

While it runs, open `.github/skills/speckit-specify/SKILL.md` and narrate what the command
is doing. It works out a short name for the feature, creates a numbered folder under
`specs/`, copies the spec template in, and records which feature is active.

Point out that **no git branch is created**. Older versions of Spec Kit cut a branch per
feature. Version 1.x keeps track of the active feature in a small file instead, which is
our next step.

**Step 5 — `.specify/feature.json`**

A single line of JSON with a `feature_directory` key. Every later command reads this to
find the feature, so it doesn't matter what branch you're on.

Check that it says `specs/001-expense-policy-validator`. The last line of the prompt
asks for that name, but the model chooses it, and every path in the rest of this
README assumes it. If the folder came out with a different name, either use that name
in place of `001-expense-policy-validator` from here on, or reset the demo (see the end
of this README) and run `/speckit-specify` again.

**Step 6 — `specs/001-expense-policy-validator/spec.md`, the anatomy tour**

This is the main event. Walk through the four required sections in order.

- **`## User Scenarios & Testing *(mandatory)*`** — three user stories, marked P1, P2 and
  P3. Each has a **Why this priority** line, an **Independent Test**, and acceptance
  scenarios written as Given, When, Then. Stress the independence rule: P1 on its own has
  to be something you could ship. That's what lets us build just one story in demo 05.
- **`## Requirements *(mandatory)*`** — the functional requirements, numbered `FR-001`
  onward, each phrased as "System MUST". Pick two and ask the audience whether they could
  write a failing test from each one without asking a follow-up question. That's the
  standard every requirement has to meet.
- **`### Key Entities`** — ExpenseSubmission, LineItem, PolicyRule and Violation. There
  are no types, no storage and no code, just what each thing represents.
- **`## Success Criteria *(mandatory)*`** — numbered `SC-001` onward, measurable and free
  of technology. Contrast one with a requirement: the requirement says what the system
  does, while the success criterion says how you'd know it worked.
- **`## Assumptions`** — the defaults the model chose so it didn't have to ask. This is
  where prompt-driven development's silent guesses get written down instead of buried.

**Step 7 — the ambiguity markers**

Search the file for `[NEEDS CLARIFICATION:`. You'll find at most three, because the
command limits itself to three and only marks things where there's no sensible default.
In our run they landed on the partial-day rule, the exchange rate, and whether a missing
receipt blocks the submission.

Compare them with `resources/reference/spec.draft.md`. These are the same three gaps from step 1.
The spec found them and said so, where the prompt-built validator in demo 01 just picked
a number.

**Step 8 — `specs/001-expense-policy-validator/checklists/requirements.md`**

`/speckit-specify` created this too. It's a quality checklist for the spec itself, with
items numbered `CHK001` onward. Several are unchecked right now, because of the markers
from step 7. Remember this file, because `/speckit-implement` reads these checkboxes later
and asks before going ahead if any are still open.

**Step 9 — run `/speckit-clarify`**

Type `/speckit-clarify` in the chat panel. It asks up to five questions, one at a time.
Each comes with a recommended answer and a short explanation of why the question matters.
Answer from `resources/prompts/clarify-answers.md`:

1. Exchange rate: the corporate monthly rate in force on the transaction date.
2. Per-diem caps: per travel day, with the first and last day at 75 percent.
3. Missing receipt above the threshold: blocking, not a warning.
4. Approval thresholds: from the policy file, at 500 and 2,500 US dollars.
5. Reporting: every violation in one pass, exit 0, 1 or 2.

The questions won't always come in this order or with this wording, so match on the
topic. If you get one that isn't listed, the prompt file has spares.

After the first answer, pause and show `spec.md` on disk before answering the next. Spec
Kit saves after each answer. You'll see a new `## Clarifications` section appear with a
dated session and a `- Q: … → A: …` line. Then scroll down and show that the same answer
also rewrote the matching `FR-` line and removed its marker. The answers aren't just
logged; they're worked back into the requirements.

**Step 10 — the checklist again**

After the last answer, reopen `checklists/requirements.md`. The clarify step re-checks
each item against the updated spec and reports a before-and-after count. Ours went from
12 of 16 to 15 of 16.

The one still unchecked is deliberate, and the note at the bottom of the file explains
why. Some judgments belong to a reviewer rather than to the tool.

**Step 11 — compare with the reference**

From the repository root, run:

```
git diff --no-index demos/03-intent-to-spec/resources/reference/spec.clarified.md demos/03-intent-to-spec/app/specs/001-expense-policy-validator/spec.md
```

The wording and ordering will differ. The decisions won't. That's the point to close on:
a spec isn't a deterministic artifact, but it is a reviewable one, and review is exactly
what prompt-driven iteration never gives you a place to do.

**Step 12 — hand off**

The next demo starts from a spec just like this one, already committed, so if your run
went sideways you can pick up there without losing anything.

## If your run differs from ours

Copilot doesn't produce the same text twice, so your requirement wording and numbering
won't match ours exactly. That's expected, and step 11 is designed to show it.

If a live step goes wrong, copy our version into place and keep going:

```
mkdir -p specs/001-expense-policy-validator/checklists
cp ../resources/reference/spec.clarified.md specs/001-expense-policy-validator/spec.md
cp ../resources/reference/checklists-requirements.md specs/001-expense-policy-validator/checklists/requirements.md
```

## Resetting between runs

From the repository root:

```
git restore demos/03-intent-to-spec
git clean -fd demos/03-intent-to-spec
```

That removes the `specs/001-…` folder and `.specify/feature.json` that the live run
created, and leaves the committed files as they were.
