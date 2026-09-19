# Demo 02 — Initialize Spec Kit and Write the Constitution

**Time:** about 9 minutes · **Part of:** on-screen segment 1

In this demo we set up Spec Kit in an empty folder and look at what it installs. Then we
write a constitution: the small set of rules that applies to every feature this project
will ever have, not just the one we're about to build.

Two steps run live here: `specify init` in the terminal, and `/speckit-constitution` in
the GitHub Copilot chat panel.

## Before you start

**Tools you'll need**

| Tool | Version | Check with |
|---|---|---|
| `uv` | 0.11 or newer | `uv --version` |
| Python | 3.13 (`uv` installs it for you) | `uv python list` |
| Visual Studio Code | current release | `code --version` |
| GitHub Copilot | signed in, with chat enabled | the Copilot icon in the VS Code status bar |
| Git | any recent version | `git --version` |

You don't install Spec Kit separately. This folder's `pyproject.toml` pins release
`1.0.8` from PyPI, and `uv sync` brings it down.

**Setup, from the `app` folder**

```
uv sync
uv run specify version
```

The version line should read `1.0.8`. If it says anything else, stop and check with
the presenter, because the command names in these demos are specific to this version.

> **A note on versions.** Most Spec Kit tutorials online were written for the 0.0.x
> releases, and several things changed in 1.x. The agent is chosen with `--integration`
> rather than `--ai`, commands are typed with hyphens as `/speckit-specify`, and no git
> branch is created per feature. If something you've read elsewhere doesn't match what
> you see here, that's almost certainly why.

## What's in this folder

| Path | What it is |
|---|---|
| `resources/acme-travel-policy.md` | The travel policy from demo 01 |
| `resources/prompts/constitution-prompt.md` | What we'll paste after `/speckit-constitution` |
| `resources/reference/constitution.md` | Our finished constitution, for comparison |
| `resources/reference/init-transcript.md` | The real console output of `specify init`, annotated |

Notice there is no `.specify/` folder and no `.github/` folder inside `app/` yet. Spec Kit
creates both.

## Presentation trail

**Step 1 — the empty folder**

List the contents of `app/` and point out what isn't there. This is where every Spec Kit
project begins, and it's worth seeing that nothing is hidden.

**Step 2 — run `specify init`**

```
uv run specify init --here --force --non-interactive --integration copilot --script py
```

Talk through the flags while it runs. `--here` initializes the current folder rather
than creating a new one. `--integration copilot` tells Spec Kit which AI tool to set up
for. `--script py` chooses the Python helper scripts, which behave the same on Windows,
macOS and Linux, so everyone following along types identical commands.

When it finishes, compare the output with `resources/reference/init-transcript.md`.
Point out the line **Constitution setup (copied from template)**, because we'll come
back to it.

**Step 3 — `app/.github/skills/`**

Open this folder in the explorer. There are ten sub-folders, each named `speckit-`
followed by a command name, and each holds a single `SKILL.md` file. These are what
Copilot loads as slash commands.

Nine of them form the workflow we'll follow today. The tenth, `speckit-taskstoissues`,
turns tasks into GitHub issues and also needs the GitHub MCP server, so we won't use it.
The Spec Kit release notes also say it's moving out of the core commands into a bundled
extension in a future release, so don't be surprised if it disappears from this list.

**Step 4 — `app/.github/skills/speckit-constitution/SKILL.md`**

Open this one and scroll through it. It's a set of instructions written for the AI tool,
in plain English. There's no hidden logic in Spec Kit's commands. What the model is told
to do is right here, and you can read it, question it and change it.

**Step 5 — `app/.specify/memory/constitution.md`**

Open it. It's full of placeholders like `[PROJECT_NAME]` and `[PRINCIPLE_1_NAME]`. That's
what "copied from template" meant in step 2. The file exists, but it doesn't say
anything yet.

**Step 6 — open the app folder in VS Code**

```
code .
```

Open the demo's **`app` folder** as the workspace, not the demo folder above it and not the
repository root. Copilot looks for skills in `.github/skills/` relative to the workspace
root, so if you open a parent folder, the `/speckit-` commands won't appear. Keeping the
workspace on `app/` also keeps `resources/` out of what Copilot can read, which matters in
a moment when we compare its constitution against ours.

Open the Copilot chat panel and type `/speckit-`. You should see all ten commands listed.
If you don't, this is almost always the reason, so check which folder is open first.

**Step 7 — run `/speckit-constitution`**

Type `/speckit-constitution` in the chat panel, then paste the text from
`resources/prompts/constitution-prompt.md`.

While it runs, go back to that prompt file and read the section "Why these five". Each
principle exists to close off one of the specific ways the demo 01 validator went wrong:
hard-coded numbers, untested requirements, floating-point money, and stopping at the
first problem.

**Step 8 — the filled constitution**

Open `.specify/memory/constitution.md` again. The placeholders are gone, and in their
place are five named principles, each with a short rationale.

Put it side by side with `resources/reference/constitution.md`. The wording won't match
exactly, because the model doesn't produce identical text twice. The principles should. If
one of yours is missing or has been softened, that's worth pointing out as a teaching
moment: the constitution is a document you review, not one you accept.

**Step 9 — why this matters**

Scroll to the Governance section at the bottom. It says the Constitution Check in the
plan must pass before research begins. That's the connection to demo 04. The rules we
just wrote aren't a note to ourselves. Every plan generated from here on gets checked
against them.

**Step 10 — hand off**

That sets the ground rules. In the next demo, we take a real feature request from Finance
and turn it into a specification that can be reviewed.

## If your run differs from ours

The model's wording will differ from our reference, and that's expected. What matters is
that the five principles are present and say what the prompt asked for.

If the run goes badly wrong, copy our version into place and carry on:

```
cp ../resources/reference/constitution.md .specify/memory/constitution.md
```

## Resetting between runs

This demo creates files, so to run it again from a clean state, go to the repository root
and run:

```
git restore demos/02-init-and-constitution
git clean -fd demos/02-init-and-constitution
```

That removes `.specify/`, `.github/` and anything else the live run created, and puts
back the committed files.
