# `specify init` transcript

This is the real console output of the command below, run against Spec Kit
release 1.0.8 from PyPI. Only the working path has been shortened for readability.

```
uv run specify init --here --force --non-interactive --integration copilot --script py
```

## What to point out

- **`Current directory is not empty (4 items)`** is expected. The four are
  `.python-version`, `pyproject.toml`, `uv.lock` and the `.venv` that `uv sync` just
  built. Spec Kit merges into the folder rather than replacing it, and `--force` is
  what skips the confirmation prompt so the demo doesn't stall.
- **`Selected coding agent integration: copilot`** confirms the `--integration`
  flag. Older tutorials show `--ai copilot`, which no longer exists in 1.x.
- **`Constitution setup (copied from template)`** means `.specify/memory/constitution.md`
  now exists but is still an unfilled template full of `[PRINCIPLE_1_NAME]`
  placeholders. `/speckit-constitution` is what fills it.
- **No git branch is created.** 1.x tracks the active feature in
  `.specify/feature.json` instead. Earlier versions cut a branch per feature.
- **The skills list** at the end is what now appears when you type `/speckit-` in
  the Copilot chat panel. Ten skills install; nine of them form the workflow. The
  tenth, `speckit-taskstoissues`, needs the GitHub MCP server, and the 1.0.7 and
  1.0.8 release notes say it is moving out of Spec Kit's core into a bundled
  extension in a future release.

## Output

```
             ███████╗██████╗ ███████╗ ██████╗██╗███████╗██╗   ██╗
             ██╔════╝██╔══██╗██╔════╝██╔════╝██║██╔════╝╚██╗ ██╔╝
             ███████╗██████╔╝█████╗  ██║     ██║█████╗   ╚████╔╝
             ╚════██║██╔═══╝ ██╔══╝  ██║     ██║██╔══╝    ╚██╔╝
             ███████║██║     ███████╗╚██████╗██║██║        ██║
             ╚══════╝╚═╝     ╚══════╝ ╚═════╝╚═╝╚═╝        ╚═╝

               GitHub Spec Kit - Spec-Driven Development Toolkit

Warning: Current directory is not empty (4 items)
Template files will be merged with existing content and may overwrite existing 
files
--force supplied: skipping confirmation and proceeding with merge
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  Specify Project Setup                                                      │
│                                                                             │
│  Project         app                                                        │
│  Working Path    demos/02-init-and-constitution/app                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Selected coding agent integration: copilot
Selected script type: py
Initialize Specify Project
├── ● Check required tools (ok)
├── ● Select coding agent integration (copilot)
├── ● Select script type (py)
├── ● Install integration (GitHub Copilot)
├── ● Install shared infrastructure (scripts (py) + templates)
├── ○ Ensure scripts executable
├── ● Constitution setup (copied from template)
├── ● Install bundled workflow (speckit installed)
└── ● Finalize (project ready)
Project ready.

┌─────────────────────────── Agent Folder Security ───────────────────────────┐
│                                                                             │
│  Some agents may store credentials, auth tokens, or other identifying and   │
│  private artifacts in the agent folder within your project.                 │
│  Consider adding .github/ (or parts of it) to .gitignore to prevent         │
│  accidental credential leakage.                                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────── Next Steps ─────────────────────────────────┐
│                                                                             │
│  1. You're already in the project directory!                                │
│  2. Start using skills with your coding agent:                              │
│     2.1 /speckit-constitution - Establish project principles                │
│     2.2 /speckit-specify - Create baseline specification                    │
│     2.3 /speckit-plan - Create implementation plan                          │
│     2.4 /speckit-tasks - Generate actionable tasks                          │
│     2.5 /speckit-implement - Execute implementation                         │
│     2.6 /speckit-converge - Assess the codebase and append remaining work   │
│  as tasks                                                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────── Enhancement Skills ─────────────────────────────┐
│                                                                             │
│  Optional skills that you can use for your specs (improve quality &         │
│  confidence)                                                                │
│                                                                             │
│  ○ /speckit-clarify (optional) - Ask structured questions to de-risk        │
│  ambiguous areas before planning (run before /speckit-plan if used)         │
│  ○ /speckit-analyze (optional) - Cross-artifact consistency & alignment     │
│  report (after /speckit-tasks, before /speckit-implement)                   │
│  ○ /speckit-checklist (optional) - Generate quality checklists to validate  │
│  requirements completeness, clarity, and consistency (after /speckit-plan)  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```
