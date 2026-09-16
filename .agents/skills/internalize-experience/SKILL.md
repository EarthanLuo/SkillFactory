---
name: internalize-experience
description: Discuss a recorded Extraction against the user's context, record the reasoning and decision, and create or update a Portable Skill only after explicit user confirmation.
metadata:
  short-description: Turn experience into a Skill deliberately
---

# Internalize Experience

Use this when the user wants to decide whether an Extraction should become part of their reusable practice.

## Read selectively

Read the relevant Extraction and Source first. Read the current `skill/SKILL.md`, its references, and related Discussions, Feedback, or Evolutions only when they affect the decision. Do not load the whole repository by default.

## Discuss

Explore whether the experience solves the user's problem, why it works, required conditions, differences between the source context and the user's context, disagreement, counterexamples, and whether to adopt, adapt, test, reject, or leave unresolved. Prefer merging useful knowledge into an existing Skill when it describes the same capability.

Record the resulting cognitive outcome using the bundled `assets/templates/DISCUSSION.md` when available, then write `memory/discussions/DSC-*.md` and update `memory/INDEX.md`. Do not force agreement when uncertainty remains.

## Portable Skill change gate

Before creating or changing `workspace/<project>/skill/`, state the proposed behavior, rationale, changed old behavior, and likely side effects. Wait for explicit user confirmation. Confirmation is required even when the change seems small.

After confirmation, keep `skill/SKILL.md` concise and self-contained. Put operational detail in `skill/references/` when useful. Never link from the Portable Skill to `../memory/`.

Do not automatically start `reverse-experience` or `evolve-skill`.
