# Skill Foundry

Skill Foundry 是一个可以作为单个 Codex 插件安装的 GitHub 仓库，用于把经验变成可复用的 Skill。

三个内置 Skill：

- `reverse-experience`：提炼可复用经验；
- `internalize-experience`：判断是否适合自己的工作；
- `evolve-skill`：真实使用后改进 Skill。

## 1. 安装一次

在 Codex 桌面应用中打开 **Plugins Directory**，选择包含 **Skill Foundry** 的 marketplace，然后点击 **Install**。

如果看不到 marketplace，先添加本仓库：

```bash
codex plugin marketplace add EarthanLuo/SkillFactory
```

然后重启 Codex，在 **Plugins Directory** 中安装 **Skill Foundry**。

## 2. 从 GitHub 更新

本仓库或你的 fork 有新提交后，运行：

```bash
codex plugin marketplace upgrade skill-foundry
```

marketplace 指向仓库根目录。整个仓库会作为一个插件更新，不需要手动复制文件。

## 3. 使用 Skill

在新的 Codex 对话中按名称调用：

```text
使用 reverse-experience 分析这篇文章：<链接或文本>
```

```text
使用 internalize-experience 讨论 EXT-20260917-001 是否适合我的项目。
```

```text
使用 evolve-skill，根据我使用 <skill-name> 后的实际结果提出改进。
```

推荐顺序：

```text
经验 → reverse-experience → internalize-experience → Skill → evolve-skill
```

这是推荐顺序，不是自动工作流。修改 Skill 前必须得到明确确认。

## 4. Fork 并创建自己的 Skill

```bash
git clone <your-fork-url>
cd SkillFactory
git remote add upstream https://github.com/EarthanLuo/SkillFactory.git
git config core.hooksPath .githooks
```

在这里开发 Skill：

```text
workspace/<project>/skill/<your-skill>/
```

项目历史放在该项目的 `memory/` 中。Skill 准备好后，pre-commit Hook 会自动复制到插件安装入口：

```text
workspace/<project>/skill/<your-skill>/
        ── pre-commit ──> skills/<your-skill>/
```

提交并推送 fork。下次 marketplace 更新时，整个仓库插件和你的 Skill 会一起更新。

不要直接编辑 `skills/` 下的生成副本。每个 Skill 的 `SKILL.md`、脚本、模板和参考资料都必须放在自己的目录内。

## 仓库结构

```text
.codex-plugin/plugin.json  插件清单
factory/                   三个内置 Skill 的源文件
skills/                    插件实际安装的 Skill
workspace/                 项目、Portable Skill 和 memory
examples/                  示例项目
.githooks/                 提交前同步脚本
```

`factory/` 和 `workspace/` 是开发源文件，`skills/` 是根插件实际加载的生成入口。

详细行为请阅读各 Skill 目录中的 README。插件市场流程见 [OpenAI 插件文档](https://developers.openai.com/plugins/build/plugins)。
