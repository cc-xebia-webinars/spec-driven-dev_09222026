# Scoped implementation

Paste this after `/speckit-implement` in the Copilot chat panel.

---

> Implement only Phase 3, tasks T009 through T015, for User Story 1. The foundational
> phase is already complete. Stop when tests/test_per_diem.py passes.

---

## Why scope it

Running `/speckit-implement` against the whole task list takes too long for a live
session and is harder to follow. Scoping to one user story's task range keeps the run
to a few minutes.

It also demonstrates the real point. The model works from a finite, written list of
tasks rather than from a chat history, so staying in scope isn't a matter of phrasing
the prompt carefully. The boundary is in `tasks.md`, and the model can see it.

## What to watch for

The foundational tasks T001 to T008 are already checked in `tasks.md`. The model
should leave those alone and tick off T009 onward as it goes. If it starts working on
User Story 2, that's worth pointing out, because it means the scope instruction was
ignored rather than the task list being unclear.
