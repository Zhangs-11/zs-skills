# zs-skills

> 先把问题的正反双方想完整，再写公众号、追 AI 热点、诊断问题、审代码、开会上汇报、画结构图……不用为每种工作流重新教 AI 一遍。

<p align="center">
  <a href="https://github.com/Zhangs-11/zs-skills/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/Zhangs-11/zs-skills?style=for-the-badge&logo=github" /></a>
  <a href="https://github.com/Zhangs-11/zs-skills/network/members"><img alt="Forks" src="https://img.shields.io/github/forks/Zhangs-11/zs-skills?style=for-the-badge&logo=github" /></a>
  <a href="https://github.com/Zhangs-11/zs-skills/issues"><img alt="Issues" src="https://img.shields.io/github/issues/Zhangs-11/zs-skills?style=for-the-badge&logo=github" /></a>
  <a href="https://github.com/Zhangs-11/zs-skills/commits/main"><img alt="Last commit" src="https://img.shields.io/github/last-commit/Zhangs-11/zs-skills?style=for-the-badge&logo=git" /></a>
  <a href="https://github.com/Zhangs-11/zs-skills/actions/workflows/skill-quality.yml"><img alt="Skill quality" src="https://img.shields.io/github/actions/workflow/status/Zhangs-11/zs-skills/skill-quality.yml?branch=main&style=for-the-badge&label=skill%20quality" /></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge" /></a>
</p>

这是一套面向 Claude Code、Codex 及其他 Agent Skills 兼容工具的中文 skills 合集。每个 skill 都把触发场景、工作流程、边界与配套资源放进独立目录，安装后直接用自然语言调用。

```bash
npx skills add Zhangs-11/zs-skills
```

## 22 个可安装 skills

| Skill | 解决什么问题 | 你可以这样说 |
|---|---|---|
| [ai-hot-picker](ai-hot-picker/) | 从当天 AI 热点中筛出适合创作的选题 | “今天写什么 AI 话题？” |
| [aihot](aihot/) | 查询最新 AI 日报、发布、论文和行业动态 | “今天 AI 圈有什么大事？” |
| [change-meeting-brief](change-meeting-brief/) | 把需求和 PR 压成 20～40 秒的会议改动口径 | “只说问题、原逻辑和这次怎么解决。” |
| [clarify-before-action](clarify-before-action/) | 复杂任务开始前先只读调查并澄清背景、需求、痛点和验收标准 | “先别动手，一次问我一个问题，确认后再做。” |
| [dating-chat-coach](dating-chat-coach/) | 相亲或线上认识后的接话、转微信、邀约与安全判断 | “她这么回，我该怎么接？” |
| [diagnose-and-explain](diagnose-and-explain/) | 用证据和可证伪假设诊断技术、业务、产品、流程与数据问题，并给小白讲清根因 | “先只读查根因，把我当小白讲明白，修复前问我。” |
| [explain-to-master](explain-to-master/) | 用具体 Case、费曼复述、单问题追问和迁移测试真正弄懂一个主题 | “看完还是似懂非懂，用一个 Case 带我走一遍。” |
| [fable-writer](fable-writer/) | 用精炼寓言解释抽象概念，并附理解检验 | “用寓言讲明白沉没成本。” |
| [first-principles-adversarial-review](first-principles-adversarial-review/) | 用第一性原理重构问题，再主动寻找反证、遗漏和错误事实源 | “别顺着我的方案，先从机制和反证审查一遍。” |
| [kakarot-repurposer](kakarot-repurposer/) | 从同一内容母稿派生小红书、抖音和B站版本 | “把这篇一稿多平台。” |
| [human-writing](kakarot-human-writing/) | 写有材料、有判断、有自然中文节奏的通用正文 | “把这些笔记写成一篇有活人感的长文。” |
| [kakarot-writer](kakarot-writer/) | 先检查材料与 AI 价值，再按 Kakarot 的个人风格完整交付长文 | “帮我按自己的风格写篇文章。” |
| [leader](leader/) | 把一句想法拆成 agent 能独立执行的目标任务书 | “把这个想法拆成可执行 brief。” |
| [life-designer](life-designer/) | 用人生设计方法生成三套五年奥德赛计划 | “我想转行，帮我系统梳理。” |
| [peer-pr-review](peer-pr-review/) | 对抗式审查代码改动，并用一个具体 Case 走通改动前后的真实链路 | “我不懂这块代码，用一个 Case 带我走完再告诉我怎么改。” |
| [project-aware-coding](project-aware-coding/) | 写代码前参考项目已有逻辑、设计与历史经验，再做贴合真实消费者的最小实现 | “参考项目现有写法帮我实现这个需求，别重复踩坑。” |
| [review-handoff](review-handoff/) | 生成可直接发给同事、必要时包含具体 Case 走读的 Markdown Review 交接说明 | “把我的 PR 整理成一份 MD，并用一个 Case 讲清链路。” |
| [resume-optimizer](resume-optimizer/) | 从零撰写、优化或评审程序员简历 | “以面试官视角评审这份简历。” |
| [steelman-before-answer](steelman-before-answer/) | 后台钢人正反双方，只把必要确认、结论和证据展示给用户 | “后台多想一层，有必要确认的再问我。” |
| [storage-analyzer](storage-analyzer/) | 只读扫描磁盘并生成分级清理报告 | “电脑空间不够，帮我看看谁占满了。” |
| [system-structure-diagram](system-structure-diagram-skill/) | 按参考图样式和真实项目模块生成结构图 | “按这张图的样式画项目结构图。” |
| [wechat-publisher](wechat-publisher/) | 隔离公开正文与交付附录，检查图片和外链后存入公众号草稿箱 | “把这篇发到公众号草稿箱。” |

## 安装

安装全部 skills：

```bash
npx skills add Zhangs-11/zs-skills
```

只安装一个：

```bash
npx skills add Zhangs-11/zs-skills --skill aihot
```

查看仓库中可发现的名称：

```bash
npx skills add Zhangs-11/zs-skills --list
```

安装后重新启动或新开一次 Claude Code / Codex 会话，让工具重新发现 skills。

## 前置条件与风险边界

- [ ] 已安装 Node.js 与 `npx`：运行 `node --version && npx --version` 验证。
- [ ] 使用 `kakarot-writer` 时同时安装 `human-writing`；如需真实素材或 AI 主视觉的双尺寸封面，再安装 `guizang-social-card-skill`。
- [ ] `system-structure-diagram` 导出 PNG 时需要浏览器或 SVG 转换工具；仅生成 SVG 时不需要 Inkscape。
- [ ] `wechat-publisher` 需要 Python 3.12+、微信公众号 AppID/AppSecret，以及已配置的 IP 白名单；写入草稿箱前会先做只读预检。
- [ ] `storage-analyzer` 的扫描阶段只读；任何删除都必须由用户单独确认，报告中的可释放空间是估算值。
- [ ] `aihot` 与 `ai-hot-picker` 会访问 AI HOT 的公开接口，不需要 API Key，但需要网络。
- [ ] `dating-chat-coach` 提供沟通建议而非操控话术；遇到诈骗或线下见面风险时以安全为先。
- [ ] `peer-pr-review` 需要能读取目标 PR、Git 工作区或 worktree，`review-handoff` 需要能读取 PR 或对应仓库；二者默认不会评论、通过、合并、commit 或 push，也不会把当前 `main` 冒充成某环境已部署版本。
- [ ] `project-aware-coding` 需要能读取目标仓库及其项目说明；它会参考现有代码和历史经验但不会机械照搬，也不会在没有当前授权时 commit、push 或部署。
- [ ] `clarify-before-action` 与 `diagnose-and-explain` 可以自主只读调查；实现、修复、写数据及其他外部变更必须在说明范围后获得明确确认。
- [ ] `steelman-before-answer` 默认不增加澄清回合；只有存在会实质改变结果的用户选择时才提问。若要稳定覆盖 Codex 与 Claude Code，需要分别在全局 `AGENTS.md` 和 `CLAUDE.md` 加入后台入口。

其余纯提示词 skills 无额外依赖。每个目录的 README 会列出更具体的输入、输出和限制。

## 仓库自动质检

每次推送到 `main`、创建 PR 或手动触发工作流时，GitHub Actions 会检查所有 Skill 的 frontmatter、目录名与 Skill 名称、`agents/openai.yaml`、评测 JSON、本地 Markdown 链接，以及 Git 中受跟踪的高置信凭据和危险凭据文件。

本地运行同一套检查：

```bash
python3 -m pip install -r scripts/requirements-ci.txt
python3 scripts/validate_repo.py
```

扫描只读取 Git 已跟踪内容，不执行各 Skill 自带脚本，也不会把文件上传到第三方扫描服务。凭据命中只显示文件与行号，不回显疑似秘密本身。

## 推荐工作流

内容生产可以串起来使用：

```text
ai-hot-picker 选题
        ↓
kakarot-writer 确定作者位置与材料，通过 AI 价值门槛
        ↓
human-writing 生成自然、可靠的正文
        ↓
kakarot-writer 完成个人复核、标题、配图与封面
        ↓
作者修改后，可比较实际初稿与终稿，生成待确认的个人偏好候选
        ↓
同一篇内容母稿发布到公众号，并同步知乎、博客、掘金、B站专栏
        ↓
kakarot-repurposer 按需派生小红书、抖音与B站视频版本
        ↓
wechat-publisher 在明确要求发布时保存公众号草稿
```

学习与执行也可以组合：看完分析仍似懂非懂时，先让 `explain-to-master` 用一个具体 Case 建立体感，再通过一次一个问题的追问和复述形成可靠理解；需要执行时，再让 `leader` 把目标拆成可验收任务书。

`steelman-before-answer` 是所有新任务的后台审查入口：内部钢人正反双方并寻找关键变量，默认只展示结论、必要证据和确实需要用户决定的一个问题。实质性任务随后由 `first-principles-adversarial-review` 提供推理底盘，再交给需求澄清、诊断、Review、编码或写作等领域 Skill 完成具体工作。只有用户明确要求时才展开完整双向钢人。

需求与问题处理可以这样分流：

```text
准备做新需求或复杂任务
        ↓
clarify-before-action 先调查并澄清背景、需求、痛点、范围与验收标准
        ↓
用户确认后再实现

已经出现异常，想知道为什么
        ↓
diagnose-and-explain 用事实源、对照和可证伪假设定位根因并讲明白
        ↓
用户确认后再修复
```

代码评审协作可以串起来使用：

```text
peer-pr-review 审查同事 PR 或自己的本地/worktree 改动，用新手白话和一个具体 Case 走通改动前/后链路
        ↓
review-handoff 把你自己的 PR 整理成可直接转发、必要时附具体 Case 的 Markdown
        ↓
change-meeting-brief 从需求、PR 或 Review 文档压出 20～40 秒会议口径
```

## 仓库结构

每个一级子目录是一项独立 skill：

```text
<skill-name>/
├── SKILL.md       # 触发描述与执行说明
├── README.md      # 面向使用者的安装和使用说明
├── scripts/       # 可选：确定性脚本
├── references/    # 可选：按需读取的参考资料
└── assets/        # 可选：模板和静态资源
```

## Troubleshooting

| 问题 | 原因 | 解决方法 |
|---|---|---|
| `No valid skills found` | `SKILL.md` frontmatter 无效，或仓库路径错误 | 先运行 `npx skills add Zhangs-11/zs-skills --list`，确认目标名称存在 |
| 安装后没有触发 | 当前会话尚未刷新 skill 清单，或提示过于模糊 | 新开会话，并使用表格中的自然语言示例重试 |
| 只想装一个 skill | 默认命令会进入多选或安装多个 | 增加 `--skill <name>`，名称以 `--list` 输出为准 |
| 脚本提示路径不存在 | skill 被安装到了不同 agent 的目录 | 优先从当前 skill 根目录解析脚本；必要时重新安装到当前 agent |
| 微信发布失败 `40164` | 当前公网 IP 未加入公众号白名单 | 在微信公众平台添加报错中的 IP，再重新执行预检与发布 |

## License

MIT。详见 [LICENSE](LICENSE)。
