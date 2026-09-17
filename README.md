# Skill Foundry

English | [中文](README.zh.md)

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

### Getting started

```bash
git clone <this-repo> && cd SkillFactory
```

The three Factory Skills are already discoverable under `.agents/skills/`, so no separate install step is required in this project. In a chat session, trigger them by name:

- “reverse-experience from this video/article: <source>”
- “internalize-experience for EXT-XXXXXXXX-XXX in my context”
- “evolve-skill from what actually happened when I used <skill>”

### Creating a new project

1. Create `workspace/<project-name>/` with a `PROJECT.md`, plus empty `skill/` and `memory/` directories.
2. Copy any Skill's `assets/templates/PROJECT.md` as a starting point.
3. Run `reverse-experience` to write `memory/sources/` and `memory/extractions/`.
4. Keep `memory/INDEX.md` updated as the traceability entry point for the project.

### Using a Portable Skill elsewhere

Copy only the Skill directory, for example `workspace/table-skills/skill/verified-project-handoff/`. It must work on its own: it may not reference `../memory/`, the workspace root, or Factory Skills. When a Chinese copy is requested, it is stored as `SKILL.zh-CN.md` beside `SKILL.md` in the same directory.

## Available Portable Skills

Both artifacts below live under `workspace/table-skills/`, which was produced from a reverse-engineering pass over an external repository and then refined through recorded feedback and evolutions. The full history is in `workspace/table-skills/memory/`.

### `verified-project-handoff`

- Path: `workspace/table-skills/skill/verified-project-handoff/`
- Purpose: on an explicit user request, compress a long-running task into the minimum facts a receiver needs, then complete a verifiable manual handoff.
- Pairs with a Chinese copy at `SKILL.zh-CN.md` in the same directory.
- Boundaries: manual trigger only, no Hooks, no auto-continuation; never writes credentials; does not claim a handoff succeeded until the receiver confirms directory, ID, artifacts, constraints, and first step.

### `chat-research-stand-in`

- Path: `workspace/table-skills/skill/chat-research-stand-in/`
- Purpose: delegate one bounded, research-heavy task to a separate desktop ChatGPT chat acting as a constrained research subagent, then wait, recover, and verify a compact decision package to protect the coordinating task's context.
- Bundled helpers: `scripts/stand_in_package.py` (deterministic task packaging and pre-model filtering) and `scripts/host_wait.mjs` (bounded host-side status waiting).
- Boundaries: experimental, desktop-host only; no Astra testing, no generic browser automation; preparing a package does not authorize sending it; external answers stay untrusted until verified.

### Example Skill

`examples/research-update/skill/` is a small, illustrative Portable Skill (`research-update`) showing a compact lifecycle: choose context by audience, lead with the decision-relevant uncertainty, and keep observation separate from inference.

## Design principles

A Chinese translation of this README is available at [`README.zh.md`](README.zh.md).

`human-triggered` · `portable` · `traceable` · `feedback-driven` · `non-automatic`

The repository intentionally uses plain Markdown and light metadata. It has no score system, user profile, database, or mandatory workflow.
