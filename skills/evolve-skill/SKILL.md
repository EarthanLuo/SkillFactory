---
name: evolve-skill
description: Capture real usage feedback for a Portable Skill, discuss its cause and a proposed change, and record an Evolution only after explicit user confirmation.
metadata:
  short-description: Evolve a Skill from real use
---

# Evolve Skill

Use this when the user reports what happened while using a Portable Skill.

## Sequence

1. Record the observed situation and experience using the bundled `assets/templates/FEEDBACK.md` when available, then write `memory/feedback/FB-*.md` before proposing a patch; update `memory/INDEX.md`.
2. Discuss why it happened and distinguish among a flawed principle, overly broad conditions, wrong trigger, inaccurate reference, heavy procedure, impractical execution, a new boundary case, poor user experience, or a mismatch between design and actual practice.
3. Propose a concrete change, including old behavior, new behavior, rationale, and side effects.
4. Wait for explicit user confirmation.
5. Only after confirmation, modify the Portable Skill, write `memory/evolution/EVO-*.md` using `assets/templates/EVOLUTION.md` when available, and update `memory/INDEX.md`.

Feedback alone is not authorization to patch. Positive feedback should also be preserved when it explains what must not be lost.

## Portability

Keep the resulting `skill/` independently usable. Do not copy raw notes, discussion records, or feedback into the Portable Skill unless their distilled content is needed for execution. Do not create scores, a user profile, or an automatic workflow.
