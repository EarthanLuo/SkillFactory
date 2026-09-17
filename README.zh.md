# Skill Foundry

[English](README.md) | 中文

Skill Foundry 是一个轻量、Markdown 优先的工作区，用于把有用的经验转化为可移植、可迭代的 Agent Skill。

它帮助你：

1. 从来源中反向拆解一段经验；
2. 讨论它是否以及如何适用于你自己的场景；
3. 仅在确认之后创建可移植 Skill；
4. 记录真实使用反馈；
5. 在后续讨论之后演进该 Skill。

## Factory Skills

- `factory/reverse-experience`：来源 → Source + Extraction。它重构问题、方法、前提假设、边界和可迁移经验。
- `factory/internalize-experience`：把一个 Extraction 放到用户场景中讨论，并记录明确的决定。只有在用户确认之后才可能创建或更新可移植 Skill。
- `factory/evolve-skill`：先记录真实反馈，再讨论某个可移植 Skill 是否应该改变。只有在确认之后才写入 Evolution 记录。

这些是由用户触发的工具。Foundry 不强制顺序、不运行自动流水线，也不维护中心化的状态机。

它们同时被放在 `.agents/skills/` 下用于项目内发现，因此在检出代码后即可使用。`factory/` 下的副本仍是便于人阅读的源布局。

## 工作区结构

`workspace/` 下的每个项目区分两件事：

- `skill/` 是当前可独立复制的可移植 Skill。
- `memory/` 是可追溯的生产历史：来源、提取、讨论、反馈和演进记录。

复制 `workspace/<project>/skill/` 必须足以在其他地方使用该 Skill，且不能引用 `../memory/`。

## 基本用法

1. 在 `workspace/` 下打开或创建一个项目。
2. 用视频、文章、论文、教程、对话或个人成功／失败经历调用 `reverse-experience`。
3. 当你想把某个想法放到自己的实际情境中检验时，调用 `internalize-experience`。
4. 只有在明确确认建议的行为之后，才创建或修改可移植 Skill。
5. 在实际工作中使用之后，用真实发生的情况调用 `evolve-skill`。任何变更建议提出之前，先记录反馈。

`examples/research-update/` 是一个紧凑的完整生命周期示例。

### 快速开始

```bash
git clone <this-repo> && cd SkillFactory
```

三个 Factory Skills 已经在 `.agents/skills/` 下可被发现，因此在本项目中无需额外的安装步骤。在对话中，按名称触发它们：

- “reverse-experience from this video/article: <来源>”
- “internalize-experience for EXT-XXXXXXXX-XXX in my context”
- “evolve-skill from what actually happened when I used <skill>”

### 创建一个新项目

1. 创建 `workspace/<project-name>/`，包含 `PROJECT.md`，以及空的 `skill/` 和 `memory/` 目录。
2. 复制任一 Skill 的 `assets/templates/PROJECT.md` 作为起点。
3. 运行 `reverse-experience` 以写入 `memory/sources/` 和 `memory/extractions/`。
4. 持续更新 `memory/INDEX.md`，作为该项目可追溯性的入口。

### 在其他地方使用可移植 Skill

只复制 Skill 目录本身，例如 `workspace/table-skills/skill/verified-project-handoff/`。它必须能独立工作：不能引用 `../memory/`、工作区根目录或 Factory Skills。当需要中文副本时，它作为 `SKILL.zh-CN.md` 与 `SKILL.md` 存放在同一目录下。

## 已有的可移植 Skill

下面两个成果位于 `workspace/table-skills/`。该项目源自对某个外部仓库的反向拆解，之后通过已记录的反馈和演进不断细化。完整历史见 `workspace/table-skills/memory/`。

### `verified-project-handoff`

- 路径：`workspace/table-skills/skill/verified-project-handoff/`
- 用途：在用户明确要求时，把一个长任务压缩为接手方真正需要的最小事实包，然后完成可核验的手动交接。
- 同目录下有中文副本 `SKILL.zh-CN.md`。
- 边界：仅手动触发，不使用 Hook，不自动继续；不写入凭据；在接手方确认目录、ID、成果物、约束和第一步之前，不声称交接已完成。

### `chat-research-stand-in`

- 路径：`workspace/table-skills/skill/chat-research-stand-in/`
- 用途：把一个边界清晰、偏研究型的任务委派给一个独立的桌面端 ChatGPT 对话，使其充当受约束的研究子代理；随后等待、回收并核验一个紧凑的决策包，以保护协调任务的上下文。
- 附带脚本：`scripts/stand_in_package.py`（确定性的任务打包与模型前置过滤）和 `scripts/host_wait.mjs`（有界的宿主端状态等待）。
- 边界：实验性，仅面向桌面宿主；不测试 Astra，不做通用浏览器自动化；准备好任务包不等于授权发送；外部回答在核验之前都视为不可信。

### 示例 Skill

`examples/research-update/skill/` 是一个小型示例性可移植 Skill（`research-update`），展示了一个紧凑的生命周期：按受众选择上下文，优先呈现与决策最相关的未确定性，并把观察与推断分开。

## 设计原则

`人工触发` · `可移植` · `可追溯` · `反馈驱动` · `非自动化`

本仓库有意使用纯 Markdown 和轻量元数据。它没有评分系统、用户画像、数据库或强制流程。
