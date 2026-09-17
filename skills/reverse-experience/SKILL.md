---
name: reverse-experience
description: Reverse-engineer a video, article, paper, tutorial, conversation, or personal success/failure into a traceable Source and Extraction without automatically adopting it or creating a Skill.
metadata:
  short-description: Extract transferable experience
---

# Reverse Experience

Use this when the user provides experience and wants to understand what is actually reusable. It is not a summary tool.

## Outcome

Create or update two Markdown artifacts in the selected Foundry project:

1. a `memory/sources/SRC-*.md` record preserving provenance and relevant source claims;
2. a `memory/extractions/EXT-*.md` record that reconstructs the problem, approach, reasoning, conditions, hidden assumptions, transferable experience, uncertainty, and possible Skill.

Use the bundled templates in `assets/templates/` when available (`PROJECT.md`, `SOURCE.md`, and `EXTRACTION.md`). Use a date plus a collision-free sequence for IDs. Update `memory/INDEX.md` for each created artifact.

## Method

- Accept many source types; do not assume the input is a video.
- Separate what the source says, what the source actually does, why it may work, and your inference about transfer.
- Preserve each source claim's scope before compressing it: retain the subject, model or version, environment, time, comparison baseline, and qualifiers when they affect the meaning. Mark an unavailable scope element as unknown; do not silently broaden it.
- Treat a result observed under one condition as evidence about that condition, not the whole approach. Keep scoped empirical results separate from judgments about whether the underlying design may still transfer.
- Ask what problem the experience solves and what judgment rule is underneath the advice.
- Identify context-specific constraints, missing premises, counterexamples, and likely failure boundaries.
- Preserve uncertainty. An Extraction is analysis, not user acceptance.
- If the project does not exist, propose a small project name and create only the project skeleton needed for the requested capture.

## Conversational handoff

After writing the Source and Extraction, bring the unresolved judgment back to the user instead of ending with file paths alone:

- briefly state what was extracted;
- surface one to three concrete tensions or questions that require the user's context or judgment;
- end with one specific question that invites the user to continue the discussion.

This handoff may invite `internalize-experience`, but it is not itself an internalization decision. Until the user responds, do not create a Discussion record, invent a user position, or choose `ADOPT`, `ADAPT`, `TEST`, `REJECT`, or `UNRESOLVED` on the user's behalf.

## Boundaries

Do not create or modify a Portable Skill, automatically invoke another Factory Skill, or infer that an experience should be adopted. You may invite `internalize-experience` as the next user-triggered action and begin that transition with a concrete question, but wait for the user's response before recording any discussion or decision.
