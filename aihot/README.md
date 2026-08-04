# AI HOT — Agent Skill

让 AI Agent 用最自然的中文一句话拿到 [aihot.virxact.com](https://aihot.virxact.com) 每天的 AI HOT 日报和全部 AI 动态，零配置。

> 跨 Claude Code · Codex CLI · Cursor · Gemini CLI · GitHub Copilot · OpenCode · Cline · Windsurf 等任意支持 SKILL.md 格式的 Agent 平台。

## 这是什么

[AI HOT](https://aihot.virxact.com) 是一个面向中文 AI 创业者的资讯站，每天早上 08:00 整理成版块化日报，全天持续抓取并 LLM 评分筛选成精选条目。

这个 Skill 让 Agent 直接调 AI HOT 的公开 REST API，不需要打开浏览器。

## 安装

一行安装到支持 Agent Skills 的工具：

```bash
npx skills add Zhangs-11/zs-skills --skill aihot
```

查看仓库内可发现的 skill 名称：

```bash
npx skills add Zhangs-11/zs-skills --list
```

安装后重新启动或新开一次 Agent 会话，让工具刷新 skill 清单。

## 触发示例

随便问，不需要记关键字：

- 今天 AI 圈有什么新东西？
- 看一下今天的 AI 日报
- 最近 OpenAI 有什么发布？
- 最近一周的 AI 论文
- 看下精选条目
- AI 模型发布列表
- 最近 3 天 AI 行业动态

Skill 会自动调用 [aihot.virxact.com](https://aihot.virxact.com) 的公开 API（无须配置 API Key），整理成中文 markdown 简报回给你。

## 不需要登录、不需要 API Key

AI HOT 的数据 100% 公开免费，匿名可访。Skill 调以下接口：

| 路径 | 用途 |
|---|---|
| `/api/public/daily` | 最新 AI HOT 日报 |
| `/api/public/daily/{YYYY-MM-DD}` | 指定日期日报 |
| `/api/public/dailies` | 日报归档索引 |
| `/api/public/items` | 全部 AI 动态（按精选 / 分类 / 时间筛选） |

进阶用法（RSS 订阅 / REST API 详细参数）见 [aihot.virxact.com/agent](https://aihot.virxact.com/agent)。

## 反馈

Skill 漏触发、漏筛选、想加新查询场景？

- 在 [aihot.virxact.com/feedback](https://aihot.virxact.com/feedback) 留言
- 或者直接在 [zs-skills issues](https://github.com/Zhangs-11/zs-skills/issues) 提交问题

## Troubleshooting

| 问题 | 原因 | 解决方法 |
|---|---|---|
| API 返回 `403` | `/api/public/*` 请求缺少浏览器 User-Agent | 按 [SKILL.md](SKILL.md) 中的示例设置 `UA` 请求头 |
| “今天”的条目跨日期 | 日报按 UTC 整日切片，不等于滚动 24 小时 | 未明确说“日报”时优先查询精选条目 |
| 安装后未触发 | 当前会话尚未刷新 skill 清单 | 新开会话并直接问“今天 AI 圈有什么” |

## License

MIT
