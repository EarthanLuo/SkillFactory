# Skill Foundry

Skill Foundry is a small, Markdown-first workspace for turning useful experience into portable, iterative Agent Skills.

It helps you:

1. reverse-engineer an experience from a source;
2. discuss whether and how it applies to your own context;
3. create a portable Skill only after confirmation;
4. record real usage feedback;
5. evolve the Skill after a later discussion.

## Factory Skills

- `factory/reverse-experience`: source → Source + Extraction. It reconstructs the problem, method, assumptions, boundaries, and transferable experience.
- `factory/internalize-experience`: discusses an Extraction against the user's context and records an explicit decision. It may create or update a Portable Skill only after user confirmation.
- `factory/evolve-skill`: records real feedback first, then discusses whether a Portable Skill should change. It writes an Evolution record only after confirmation.

These are user-triggered tools. Foundry does not enforce a sequence, run an automatic pipeline, or maintain a central state machine.

They are also bundled for project-local discovery under `.agents/skills/`, so this project is ready to use after checkout. The `factory/` copies remain the human-readable source layout.

## Workspace

Each project under `workspace/` separates two concerns:

- `skill/` is the current, independently copyable Portable Skill.
- `memory/` is the traceable production history: sources, extractions, discussions, feedback, and evolution records.

Copying `workspace/<project>/skill/` must be sufficient to use the Skill elsewhere. It must not refer to `../memory/`.

## Basic usage

1. Open or create a project under `workspace/`.
2. Invoke `reverse-experience` with a video, article, paper, tutorial, conversation, or personal success/failure.
3. Invoke `internalize-experience` when you want to test the idea against your own situation.
4. Create or change the Portable Skill only after explicitly confirming the proposed behavior.
5. After using it in real work, invoke `evolve-skill` with what happened. Feedback is recorded before any change is proposed.

See `examples/research-update/` for a compact complete lifecycle.

## Design principles

`human-triggered` · `portable` · `traceable` · `feedback-driven` · `non-automatic`

The repository intentionally uses plain Markdown and light metadata. It has no score system, user profile, database, or mandatory workflow.
