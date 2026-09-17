---
name: verified-project-handoff
description: When the user explicitly requests saving and handing off a long-running task, compress the current state into minimal recovery facts and complete a verifiable manual handoff; do not trigger from ordinary continuation or context compaction.
metadata:
  short-description: Verifiable manual long-task handoff
---

# Verifiable Project Handoff

Use this Skill for one explicitly requested manual handoff. Compress the current task into facts the receiving task actually needs, then verify the handoff. Do not install, publish, delete, commit, or change unrelated configuration, and do not trigger from Hooks.

## Trigger boundary

- Run only when the user explicitly requests saving and handing off, creating a receiving task and continuing, or explicitly invokes this Skill.
- Ordinary “continue,” compaction alone, reminders, and read-only status checks do not trigger a handoff.
- One explicit invocation covers saving, creating, verifying, sending the continuation instruction, and opening the receiving task within this Skill. Stop at actions outside the original authorization.

## Workflow

1. **Gather facts.** Keep only what is needed to resume: goal and acceptance criteria, working directory and version, authoritative materials, confirmed decisions and constraints, agent suggestions, unresolved questions, progress marked done/in progress/not started/unverified, artifact locations, running tasks, next step, prerequisites, and verification method. Write “unconfirmed” for unknowns and “unverified” for unchecked claims; do not copy the full chat.
2. **Write to the existing carrier.** Prefer an incremental update to the project’s existing state file. If none exists, use `PROJECT_STATE.md` at the project root. Re-read the target before writing and merge concurrent changes; never overwrite another task with an old copy. Do not write credentials.
3. **Read back and verify.** Confirm the file was written, the path is correct, references are accessible, and decisions and next steps match the user’s request. Record one unique handoff ID and distinguish `materials checked`, `awaiting receiver verification`, `ready to continue`, `handed off`, and `blocked`.
4. **Create the receiving entry point.** If task creation is available, create exactly one receiving task whose opening instruction requests a read-only check of the directory, handoff ID, key artifacts, constraints, and first step. If creation is unavailable, provide a copyable manual opening message and artifact path. Do not create duplicates when a receipt is ambiguous.
5. **Transfer write authority after verification.** Send a clear continuation instruction only after the receiver confirms the directory, ID, versions/artifacts, constraints, and first step, with no blocking discrepancy. Report `created/dispatched; continuation pending verification` separately from `handed off`; a reply saying only “ready to start” is insufficient evidence.
6. **Finish or degrade safely.** Verify the first real action or task status. If verification fails, a tool is unavailable, permission is missing, or a result is unknown, preserve the accurate state and manual entry point; do not blindly retry or let source and receiving tasks modify the same business files in parallel.

## Handoff record template

```markdown
Handoff ID:
Source task / working directory:
Goal and acceptance criteria:
Key files, versions, and artifacts:
Confirmed decisions and constraints:
Agent suggestions / local choices:
Unresolved and unknown:
Progress (done / in progress / not started / unverified):
Next step and verification method:
Authorized scope:
Receiving task:
Handoff status: materials checked | awaiting receiver verification | ready to continue | handed off | blocked
```

## Output requirements

Start with a brief handoff status, evidence, and first step, then provide the artifact path or receiving-task entry point. Do not present suggestions as user decisions, saving or creation as a completed handoff, or unverified content as restored context.
