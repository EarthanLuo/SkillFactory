# Verified Project Handoff

## What this Skill does

`verified-project-handoff` saves the minimum verified facts needed to resume a long-running task, creates or provides a receiving entry point, and transfers continuation authority only after the receiver verifies the handoff.

It is a manual handoff Skill, not a general continuation mechanism. It does not install, publish, delete, commit, or change unrelated configuration.

## Installation

Install it as part of the `Skill Foundry` plugin from Codex's **Plugins Directory**. For a fork or local marketplace, run `codex plugin marketplace add <owner>/<repo>`, restart Codex, select the marketplace, and choose **Install**. For standalone use, copy this complete directory so both README files and the Skill definition remain together.

## When it triggers

Use it only when the user explicitly asks to save and hand off work, create a receiving task and continue, or explicitly invokes this Skill.

Do not trigger it for ordinary “continue” requests, context compaction, reminders, or read-only status checks.

## What the handoff captures

The handoff record should contain only what the receiving task needs:

- goal and acceptance criteria;
- working directory and version;
- authoritative files, artifacts, and relevant references;
- confirmed decisions, constraints, and authorized scope;
- agent suggestions kept separate from user decisions;
- unresolved items and unknowns;
- progress marked `done`, `in progress`, `not started`, or `unverified`;
- next step, prerequisites, and verification method;
- a unique handoff ID and explicit handoff status.

Never copy the full chat or write credentials into the handoff record.

## Verification workflow

1. Read the existing state carrier before writing and merge concurrent changes.
2. Prefer the project's existing state file; otherwise use `PROJECT_STATE.md` at the project root.
3. Read the file back and confirm its path, references, decisions, constraints, and next step.
4. Create exactly one receiving task when task creation is available. If it is unavailable, provide a copyable manual opening message and artifact path.
5. Ask the receiver to perform a read-only check of the directory, handoff ID, key artifacts, constraints, and first step.
6. Transfer write authority only after the receiver confirms those facts and no blocking discrepancy remains.
7. Verify the first real action or task status. If anything is unknown, preserve the accurate state and manual entry point.

## Status vocabulary

Keep these states distinct:

```text
materials checked
awaiting receiver verification
ready to continue
handed off
blocked
```

“Created” or “dispatched” is not the same as “handed off.” A reply such as “ready to start” is not sufficient evidence of receiver verification.

## Hard boundaries

- One explicit invocation covers only the authorized handoff actions.
- Do not create duplicate receiving tasks after an ambiguous receipt.
- Do not let source and receiving tasks modify the same business files in parallel.
- Do not claim a handoff succeeded until the receiver verifies the directory, ID, artifacts, constraints, and first step.
- If a tool, permission, or verification step is unavailable, degrade to a precise manual entry point instead of guessing.

## Portability

This Skill is self-contained. Keep `SKILL.md`, this README, and `README.zh-CN.md` together when copying or installing it. The Skill must not depend on the project's `memory/` directory or on another Skill.
