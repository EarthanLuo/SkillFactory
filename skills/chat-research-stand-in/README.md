# Chat Research Stand-in

## What this Skill does

`chat-research-stand-in` delegates one bounded, research-heavy task to a separate ChatGPT desktop chat, then recovers and verifies a compact decision package without importing the whole working transcript into the coordinating task.

This is an experimental desktop-host Skill. It is designed to protect the main task's context while leaving the final decision and project authority with the coordinating task and the user.

## Installation

Install it as part of the `Skill Foundry` plugin from Codex's **Plugins Directory**. If you use a fork or a local marketplace, add that marketplace with `codex plugin marketplace add <owner>/<repo>`, restart Codex, then select the marketplace and choose **Install**. For standalone use, copy this complete directory; do not copy only `SKILL.md` because the helper scripts are required for the bundled workflow.

## When to use it

Use it when:

- the research objective and source scope can be bounded;
- the work is substantial enough to justify a separate chat;
- the expected result can be returned as a compact evidence-backed package;
- the desktop host can create, identify, open, and read a ChatGPT chat.

Keep the work in the main task when it is a short question, tightly coupled to changing local files, requires frequent clarification, or needs most of the current conversation context.

## Standard workflow

1. Choose a fresh quick chat, or verify an exact existing ChatGPT desktop chat.
2. Prepare a package with the objective, acceptance criteria, authoritative materials, constraints, research scope, delegated authority, output shape, evidence budget, and forbidden actions.
3. Do not send the package unless the user explicitly authorizes submission.
4. Record a unique task ID, route, conversation identity, and submission status.
5. Wait through one bounded host-side waiter when available; do not resubmit after an ambiguous timeout.
6. Recover only the newest matching assistant result, remove host-internal citation placeholders, and keep the raw transcript out of the main context.
7. Verify important claims against the requested evidence and project state before adoption.
8. Return a compact adoption note with verified conclusions, limitations, artifacts, and the next action.

## Bundled helpers

- `scripts/stand_in_package.py` prepares packages and provides deterministic `probe`, `extract`, `budget`, `clean`, and `ledger` operations. It does not send messages, browse, verify facts, or authorize changes.
- `scripts/host_wait.mjs` provides bounded host-side waiting. The desktop host must inject its native `readThread` operation.

If Python is unavailable, the Skill can still be followed manually; the helper is not a prerequisite.

## Hard boundaries

- Do not use this Skill for ordinary browsing, generic browser automation, Astra testing, or API Conversations.
- A desktop ChatGPT conversation is not an API `conv_...` object.
- Preparing a package does not authorize sending it.
- The stand-in may research within scope, but may not change the objective, modify local files, contact third parties, spend money, handle credentials, or make the user's final decision unless separately authorized.
- A sent task is not a completed task, and a returned answer is not verified evidence.
- Do not claim token savings or quality improvements without a repeatable evaluation.

## Portability

This Skill is self-contained. Keep `SKILL.md`, this README, and both files under `scripts/` together when copying or installing it. Do not make it depend on the project's `memory/` directory or other Skills.
