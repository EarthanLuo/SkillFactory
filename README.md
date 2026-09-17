# Skill Foundry

Skill Foundry is a GitHub repository that installs as one Codex plugin. It helps turn experience into reusable Skills.

The three built-in Skills are:

- `reverse-experience` — extract a reusable idea;
- `internalize-experience` — decide whether it fits your work;
- `evolve-skill` — improve a Skill after real use.

## 1. Install once

In the Codex desktop app, open **Plugins Directory**, choose the marketplace that contains **Skill Foundry**, and click **Install**.

If the marketplace is not listed, add this repository first:

```bash
codex plugin marketplace add EarthanLuo/SkillFactory
```

Then restart Codex and install **Skill Foundry**.

## 2. Update from GitHub

After new commits are pushed to this repository or your fork:

```bash
codex plugin marketplace upgrade skill-foundry
```

The marketplace points to the repository root. The whole repository is updated as one plugin; no manual copying is needed.

## 3. Use the Skills

Call a Skill by name in a new Codex chat:

```text
Use reverse-experience on this article: <link or text>
```

```text
Use internalize-experience for EXT-20260917-001 in my project.
```

```text
Use evolve-skill based on what happened when I used <skill-name>.
```

Recommended order:

```text
experience → reverse-experience → internalize-experience → Skill → evolve-skill
```

This is a recommendation, not an automatic workflow. A Skill changes only after explicit confirmation.

## 4. Fork and create your own Skills

```bash
git clone <your-fork-url>
cd SkillFactory
git remote add upstream https://github.com/EarthanLuo/SkillFactory.git
git config core.hooksPath .githooks
```

Develop a Skill here:

```text
workspace/<project>/skill/<your-skill>/
```

Keep its history in the project's `memory/` directory. When the Skill is ready, the pre-commit hook automatically copies it to the installable surface:

```text
workspace/<project>/skill/<your-skill>/
        ── pre-commit ──> skills/<your-skill>/
```

Commit and push your fork. The next marketplace upgrade installs the updated repository, including your Skill.

Do not edit generated copies under `skills/`. Every Skill must keep its `SKILL.md`, scripts, templates, and references inside its own directory.

## Repository layout

```text
.codex-plugin/plugin.json  plugin manifest
factory/                   source of the three built-in Skills
skills/                    installable Skill surface
workspace/                 projects, Portable Skills, and memory
examples/                  example project
.githooks/                 pre-commit synchronization
```

`factory/` and `workspace/` are authoring sources. `skills/` is the generated install surface consumed by the root plugin.

For detailed behavior, read the README inside each Skill directory. See the [official OpenAI plugin documentation](https://developers.openai.com/plugins/build/plugins) for marketplace details.
