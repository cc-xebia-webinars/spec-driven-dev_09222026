# Demos

These six demos follow one feature, an expense policy validator, from a vague request all
the way to working, tested code. Each demo folder is a self-contained checkpoint: it
contains everything the earlier demos produced, so you can start at any of them without
running the ones before it.

| # | Demo | What it shows | Time |
|---|---|---|---|
| 01 | [Prompt vs. Spec](./01-prompt-vs-spec/README.md) | A validator built from a single prompt fails 7 of 11 policy tests, and why | 9 min |
| 02 | [Initialize and Write the Constitution](./02-init-and-constitution/README.md) | What `specify init` installs, and the rules that apply to every feature | 9 min |
| 03 | [From Intent to a Reviewable Spec](./03-intent-to-spec/README.md) | A Finance request becomes a spec; ambiguity is flagged and then resolved | 16 min |
| 04 | [Plan, Tasks, and a Consistency Check](./04-plan-and-tasks/README.md) | The plan is checked against the constitution and broken into ordered tasks | 14 min |
| 05 | [Implement, Then Change the Spec](./05-implement-and-iterate/README.md) | Copilot builds from the task list; a policy change flows through the spec first | 14 min |
| 06 | [The Finished Validator](./06-finished-validator/README.md) | Every requirement traced to its task, module and tests | 4 min |

During the webinar these run as four segments, one after each demo slide: demos 01 and 02
together, then 03, then 04, then 05 and 06 together.

## How each demo folder is laid out

Every demo has the same three things in it.

```
demos/NN-name/
├── README.md     the instructions and the presentation trail
├── resources/    what you read from and paste into Copilot
│   ├── acme-travel-policy.md
│   ├── prompts/      the text to paste after each /speckit- command
│   └── reference/    our finished version, for comparison and recovery
└── app/          the project itself — open this one in VS Code
```

Work inside `app/`. That's where `uv sync` runs, where Spec Kit installs itself, and where
the spec, the plan and the code end up. Keeping `resources/` outside it isn't just tidiness:
Copilot reads the folder you have open, so our finished spec and constitution stay out of
its reach and it has to do the work for itself.

## What you'll need

| Tool | Needed for |
|---|---|
| [`uv`](https://docs.astral.sh/uv/) 0.11 or newer | Every demo |
| Python 3.13 | Every demo (`uv` installs it for you) |
| [Visual Studio Code](https://code.visualstudio.com/) | Demos 02 to 05 |
| [GitHub Copilot](https://github.com/features/copilot), signed in with chat enabled | Demos 02 to 05 |
| Git | Resetting demos between runs |

You don't need to install Spec Kit yourself. Each demo that uses it pins Spec Kit
release `1.0.8` from PyPI in its `app/pyproject.toml`, and `uv sync` brings it down. That pin
matters: Spec Kit releases every few days, and the command names in these demos were
checked against this version. To use the same version outside the demos, run
`uv tool install specify-cli==1.0.8`.

## Three things that trip people up

**Open the demo's `app` folder in VS Code, not the demo folder or the repository root.**
Copilot looks for the Spec Kit commands in `.github/skills/` relative to whatever folder is
open, and that folder is `app`. If you open a parent folder, typing `/speckit-` in the chat
panel shows nothing. This is by far the most common problem.

**Commands use hyphens.** In Spec Kit 1.x you type `/speckit-specify`, not `/specify` or
`/speckit.specify`. Most tutorials online were written for the older 0.0.x releases and
show the old names. The agent is also chosen with `--integration copilot` now, not `--ai`.

**Don't install Spec Kit's `git` extension in these folders.** It runs `git init` when you
write a constitution, which would create a repository inside this one. Spec Kit 1.x
doesn't need it: it tracks the active feature in `.specify/feature.json` rather than
through git branches.

## Checking a demo folder works

Start with `uv sync` inside the demo's `app` folder. What to run next depends on the demo:

| Demo | Commands | Expected result |
|---|---|---|
| 01 | `uv run pytest` | 7 failed, 4 passed — this is the point of the demo |
| 02, 03, 04 | `uv run specify version` | `1.0.8`. These folders hold specifications rather than code, so there are no tests and pytest isn't installed. |
| 05 | `uv run specify version`<br>`uv run pytest` | `1.0.8`, then some failures before the implementation step, by design. All pass afterwards. |
| 06 | `uv run specify version`<br>`uv run pytest` | `1.0.8`, then 38 passed |

## Resetting a demo

Demos 02 to 05 create and change files as you run them. To put one back to its starting
state, go to the repository root and run, for example:

```
git restore demos/03-intent-to-spec
git clean -fd demos/03-intent-to-spec
```

## Your results will differ from ours, and that's expected

GitHub Copilot doesn't produce the same text twice, so your specs, plans and code won't
match ours word for word. Each demo keeps our version in its `resources/reference/` folder.
Compare against it for the decisions rather than the wording, and if a live step goes
wrong, each demo's README shows how to copy the reference into place and carry on.
