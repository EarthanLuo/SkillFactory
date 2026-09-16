# Working rules

- Keep this repository Markdown-first, human-readable, and easy to copy.
- Preserve the distinction between `skill/` and `memory/`.
- Factory Skills may read and write project memory as part of their explicitly requested work.
- A Portable Skill must not depend on files outside its own `skill/` directory.
- Never modify a Portable Skill from feedback alone. Discuss the proposed change and require explicit user confirmation first.
- Do not introduce a central state machine, automatic phase transitions, scoring system, or permanent user profile without a new, explicit scope decision.
- Keep source claims, user interpretation, and new inference visibly distinct.

## Agent Skills directory standard

- Every portable Skill is a self-contained directory with a required `SKILL.md` at its root.
- `SKILL.md` must begin with YAML frontmatter containing at least `name` and `description`, followed by Markdown instructions.
- Supporting resources belong inside that Skill directory. Use `scripts/` for executable helpers, `references/` for on-demand documentation, and `assets/` for static resources such as templates, examples, images, or schemas.
- A Skill must not depend on files outside its own directory. References from `SKILL.md` must use paths relative to the Skill root.
- Root-level shared folders such as `templates/` must not be treated as Skill resources. If a template is needed by a Skill, place it under that Skill's `assets/templates/` and keep any bundled copy synchronized.
- Add only resources that the Skill actually uses; do not create empty convention directories or copy unrelated templates into a Skill.
- Keep `SKILL.md` concise and load detailed material from its bundled resources only when needed.
- For newly generated Portable Skills, keep `SKILL.md` as the English default and, when a Chinese copy is requested, add only `SKILL.zh-CN.md` beside it in the same Skill directory; do not create a second Chinese Skill directory. Keep both Markdown files aligned in behavior and boundaries.
