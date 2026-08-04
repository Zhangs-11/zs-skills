# zs-skills

> 写公众号、追 AI 热点、做多平台分发、画结构图、清理磁盘……不用为每种工作流重新教 AI 一遍。

<p align="center">
  <a href="https://github.com/Zhangs-11/zs-skills/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/Zhangs-11/zs-skills?style=for-the-badge&logo=github" /></a>
  <a href="https://github.com/Zhangs-11/zs-skills/network/members"><img alt="Forks" src="https://img.shields.io/github/forks/Zhangs-11/zs-skills?style=for-the-badge&logo=github" /></a>
  <a href="https://github.com/Zhangs-11/zs-skills/issues"><img alt="Issues" src="https://img.shields.io/github/issues/Zhangs-11/zs-skills?style=for-the-badge&logo=github" /></a>
  <a href="https://github.com/Zhangs-11/zs-skills/commits/main"><img alt="Last commit" src="https://img.shields.io/github/last-commit/Zhangs-11/zs-skills?style=for-the-badge&logo=git" /></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge" /></a>
</p>

这是一套面向 Claude Code、Codex 及其他 Agent Skills 兼容工具的中文 skills 合集。每个 skill 都把触发场景、工作流程、边界与配套资源放进独立目录，安装后直接用自然语言调用。

```bash
npx skills add Zhangs-11/zs-skills
```

## 13 个可安装 skills

| Skill | 解决什么问题 | 你可以这样说 |
|---|---|---|
| [ai-hot-picker](ai-hot-picker/) | 从当天 AI 热点中筛出适合创作的选题 | “今天写什么 AI 话题？” |
| [aihot](aihot/) | 查询最新 AI 日报、发布、论文和行业动态 | “今天 AI 圈有什么大事？” |
| [dating-chat-coach](dating-chat-coach/) | 相亲或线上认识后的接话、转微信、邀约与安全判断 | “她这么回，我该怎么接？” |
| [explain-to-master](explain-to-master/) | 用费曼学习法、反例和迁移测试真正弄懂一个主题 | “我好像懂了，考考我。” |
| [fable-writer](fable-writer/) | 用精炼寓言解释抽象概念，并附理解检验 | “用寓言讲明白沉没成本。” |
| [kakarot-repurposer](kakarot-repurposer/) | 把公众号长文改成小红书笔记和抖音脚本 | “把这篇一稿多平台。” |
| [kakarot-writer](kakarot-writer/) | 按「卡卡罗特学AI」风格写公众号长文 | “按我的风格写篇公众号文章。” |
| [leader](leader/) | 把一句想法拆成 agent 能独立执行的目标任务书 | “把这个想法拆成可执行 brief。” |
| [life-designer](life-designer/) | 用人生设计方法生成三套五年奥德赛计划 | “我想转行，帮我系统梳理。” |
| [resume-optimizer](resume-optimizer/) | 从零撰写、优化或评审程序员简历 | “以面试官视角评审这份简历。” |
| [storage-analyzer](storage-analyzer/) | 只读扫描磁盘并生成分级清理报告 | “电脑空间不够，帮我看看谁占满了。” |
| [system-structure-diagram](system-structure-diagram-skill/) | 按参考图样式和真实项目模块生成结构图 | “按这张图的样式画项目结构图。” |
| [wechat-publisher](wechat-publisher/) | 把 Markdown 文章预检、配图并存入公众号草稿箱 | “把这篇发到公众号草稿箱。” |

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
- [ ] `system-structure-diagram` 导出 PNG 时需要浏览器或 SVG 转换工具；仅生成 SVG 时不需要 Inkscape。
- [ ] `wechat-publisher` 需要 Python 3.12+、微信公众号 AppID/AppSecret，以及已配置的 IP 白名单；写入草稿箱前会先做只读预检。
- [ ] `storage-analyzer` 的扫描阶段只读；任何删除都必须由用户单独确认，报告中的可释放空间是估算值。
- [ ] `aihot` 与 `ai-hot-picker` 会访问 AI HOT 的公开接口，不需要 API Key，但需要网络。
- [ ] `dating-chat-coach` 提供沟通建议而非操控话术；遇到诈骗或线下见面风险时以安全为先。

其余纯提示词 skills 无额外依赖。每个目录的 README 会列出更具体的输入、输出和限制。

## 推荐工作流

内容生产可以串起来使用：

```text
ai-hot-picker 选题
        ↓
kakarot-writer 写公众号长文
        ↓
kakarot-repurposer 改小红书与抖音版本
        ↓
wechat-publisher 预检并保存公众号草稿
```

学习与执行也可以组合：先用 `explain-to-master` 建立可靠理解，再让 `leader` 把目标拆成可验收任务书。

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
