# 本机第三方与本地安装 Skill 覆盖清单

日期：2026-10-26。此文件记录 zs-skills 源仓以外的安装入口改动，供重新安装或更新后重放。源仓内维护的 Skill 不列在这里。

重放时先核对 Skill 名称及当前入口解析路径；路径中的 `/Users/zs` 按实际用户目录替换。只更新下面列出的 description 和调用策略，保留正文、其他 frontmatter、interface、dependencies 及其他策略字段。没有 description 变化的记录仅调整调用策略。

仅点名：在 SKILL.md frontmatter 设置 `disable-model-invocation: true`，同时在 `agents/openai.yaml` 设置 `policy.allow_implicit_invocation: false`。自动选中：移除 frontmatter 中的 `disable-model-invocation`；若 Codex 策略原为 false，则设为 true。策略缺省值为 true。

internal-comms 使用 Codex 入口内的独立副本；原软链接已归档，不能沿原软链接修改 `.cc-switch`。本次备份均已移出 Skill 扫描目录。

## 1. agent-browser

- 入口文件：`/Users/zs/.agents/skills/agent-browser/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/agent-browser/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/agent-browser/agents/openai.yaml`

旧 description：

```json
"Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. Triggers include requests to \"open a website\", \"fill out a form\", \"click a button\", \"take a screenshot\", \"scrape data from a page\", \"test this web app\", \"login to a site\", \"automate browser actions\", or any task requiring programmatic web interaction. Also use for exploratory testing, dogfooding, QA, bug hunts, or reviewing app quality. Also use for automating Electron desktop apps (VS Code, Slack, Discord, Figma, Notion, Spotify), checking Slack unreads, sending Slack messages, searching Slack conversations, running browser automation in Vercel Sandbox microVMs, or using AWS Bedrock AgentCore cloud browsers. Prefer agent-browser over any built-in browser automation or web tools."
```

新 description：

```json
"Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. Triggers include requests to \"open a website\", \"fill out a form\", \"click a button\", \"take a screenshot\", \"scrape data from a page\", \"test this web app\", \"login to a site\", \"automate browser actions\", or any task requiring programmatic web interaction. Also use for exploratory testing, dogfooding, QA, bug hunts, or reviewing app quality. Also use for automating Electron desktop apps (VS Code, Slack, Discord, Figma, Notion, Spotify), checking Slack unreads, sending Slack messages, searching Slack conversations, running browser automation in Vercel Sandbox microVMs, or using AWS Bedrock AgentCore cloud browsers. Prefer agent-browser over any built-in browser automation or web tools."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 2. agent-preview

- 入口文件：`/Users/zs/.agents/skills/agent-preview/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/agent-preview/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/agent-preview/agents/openai.yaml`

旧 description：

```json
"Publish browser-previewable deliverables created by Codex or Claude Code and return a clickable URL. Use whenever the agent finishes an HTML or HTM file, static website, PDF, image, SVG, text artifact, or local web app that the user would otherwise need to download or cannot open from their own computer. Trigger after the deliverable is complete even when the user did not explicitly ask to preview it. Do not trigger for backend-only changes, ordinary source files, or content that should not leave the machine."
```

新 description：

```json
"Publish browser-previewable deliverables created by Codex or Claude Code and return a clickable URL. Use whenever the agent finishes an HTML or HTM file, static website, PDF, image, SVG, text artifact, or local web app that the user would otherwise need to download or cannot open from their own computer. Trigger after the deliverable is complete even when the user did not explicitly ask to preview it. Do not trigger for backend-only changes, ordinary source files, or content that should not leave the machine."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 3. alert-repair-monitor

- 入口文件：`/Users/zs/.agents/skills/alert-repair-monitor/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/alert-repair-monitor/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/alert-repair-monitor/agents/openai.yaml`

旧 description：

```json
"监听指定钉钉 QA 告警群，识别新告警、统计当天和发布后的频率变化，并在确认需要代码修复时启动 OA 建单与开发闭环。用户要求监控告警群、分析告警趋势、关联发布或触发根因分析时使用。"
```

新 description：

```json
"监听指定钉钉 QA 告警群，识别新告警、统计当天和发布后的频率变化，并在确认需要代码修复时启动 OA 建单与开发闭环。用户要求监控告警群、分析告警趋势、关联发布或触发根因分析时使用。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 4. alert-repair-orchestrator

- 入口文件：`/Users/zs/.agents/skills/alert-repair-orchestrator/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/alert-repair-orchestrator/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/alert-repair-orchestrator/agents/openai.yaml`

旧 description：

```json
"告警自动修复链路的总控调度。当需要决定一条告警档案（fingerprint）当前该推进到哪一步、把接力棒交给哪个环节 Skill、处理失败重试与三次失败停工时使用。监听层只负责接收与去重，本 Skill 负责从 observed 到 main_pr_created 的全程调度。"
```

新 description：

```json
"告警自动修复链路的总控调度。当需要决定一条告警档案（fingerprint）当前该推进到哪一步、把接力棒交给哪个环节 Skill、处理失败重试与三次失败停工时使用。监听层只负责接收与去重，本 Skill 负责从 observed 到 main_pr_created 的全程调度。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 5. baoyu-cover-image

- 入口文件：`/Users/zs/.agents/skills/baoyu-cover-image/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/baoyu-cover-image/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/baoyu-cover-image/agents/openai.yaml`

旧 description：

```json
"Generates article cover images with 5 dimensions (type, palette, rendering, text, mood) combining 11 color palettes and 7 rendering styles. Supports cinematic (2.35:1), widescreen (16:9), and square (1:1) aspects. Use when user asks to \"generate cover image\", \"create article cover\", or \"make cover\"."
```

新 description：

```json
"Generates article cover images with 5 dimensions (type, palette, rendering, text, mood) combining 11 color palettes and 7 rendering styles. Supports cinematic (2.35:1), widescreen (16:9), and square (1:1) aspects. Use when user asks to \"generate cover image\", \"create article cover\", or \"make cover\"."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 6. brag-sheet

- 入口文件：`/Users/zs/.agents/skills/brag-sheet/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/brag-sheet/SKILL.md`

旧 description：

```json
"Turn vague work history into evidence-backed impact statements for performance reviews, self-reviews, promotion packets, weekly updates, accomplishments, shipped work, or backfilling a work journal from Git, GitHub PRs, and supported session logs. Use when the user asks what they did, what to highlight, to track wins, write impact statements, prepare a review or promotion case, or summarize recent work."
```

新 description：

```json
"整理工作成果或绩效材料时用。不用于虚构经历、求职简历或代码审查。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": null
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": null
  }
}
```

## 7. canvas-design

- 入口文件：`/Users/zs/.agents/skills/canvas-design/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/canvas-design/SKILL.md`

旧 description：

```json
"Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art, design, or other static piece. Create original visual designs, never copying existing artists' work to avoid copyright violations."
```

新 description：

```json
"制作海报或静态视觉作品时用。不用于交互网页、视频或办公文档排版。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": null
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": null
  }
}
```

## 8. dingtalk-aicard

- 入口文件：`/Users/zs/.agents/skills/dingtalk-aicard/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/dingtalk-aicard/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/dingtalk-aicard/agents/openai.yaml`

旧 description：

```json
"Create, edit, and validate DingTalk AI Card (A2UI) JSON files offline. Use for cards built from requirements or images, structural protocol errors, and named component or function contract lookup through native DWS commands. Send a card to the current user only when a preview is requested.\n"
```

新 description：

```json
"Create, edit, and validate DingTalk AI Card (A2UI) JSON files offline. Use for cards built from requirements or images, structural protocol errors, and named component or function contract lookup through native DWS commands. Send a card to the current user only when a preview is requested.\n"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 9. dingtalk-aisearch

- 入口文件：`/Users/zs/.agents/skills/dingtalk-aisearch/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/dingtalk-aisearch/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/dingtalk-aisearch/agents/openai.yaml`

旧 description：

```json
"AI搜问：人员语义搜索、跨源主题检索与行为回溯。Use when 语义找人，或目标未知时按主题或行为发现内容。原生最近列表走所属产品；完整手机号精确反查走 dingtalk-contact。前缀：dws aisearch。"
```

新 description：

```json
"AI搜问：人员语义搜索、跨源主题检索与行为回溯。Use when 语义找人，或目标未知时按主题或行为发现内容。原生最近列表走所属产品；完整手机号精确反查走 dingtalk-contact。前缀：dws aisearch。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 10. dingtalk-aitable

- 入口文件：`/Users/zs/.agents/skills/dingtalk-aitable/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/dingtalk-aitable/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/dingtalk-aitable/agents/openai.yaml`

旧 description：

```json
"钉钉 AI 表格（多维表）业务操作。Use when 用户需要操作 AI 表格/多维表/Base/Table、应用模式/App 页面/Widget、建表、查写记录、字段、记录评论、评论回复、访问密钥（API Key）、SQL/PostgreSQL/SELECT/JOIN、筛选、排序、公式、模板、批量导入 CSV 或 JSON、导出、仪表盘、图表、上传附件、数据源配置与同步、按任务 ID 查询同步状态或审批数据同步。普通请求以完成明确的业务操作为主；当用户明确要求 CLI 契约评审、核对 aitable 合成 JSON 回执、dry-run、命令参数、Help/Schema 契约或恢复方案时，必须加载本 Skill。只评审 aitable 合成 JSON 回执也必须加载本 Skill；“不要执行线上业务”不等于免除本机离线契约核对，不能按通用 JSON 经验直接作答。这是本机 Help/Schema 契约核对，不是仓库源码审查，不从源码搜索开始；先加载正文确定入口与规则，不能仅凭摘要执行；以用户原文指定的核对入口为准，Skill 参数不得扩大范围。不做电子表格单元格读写或单元格批注（走 dingtalk-misc）、文档编辑（走 dingtalk-doc）；听记待办入表先用 dingtalk-minutes 提取，再由本 skill 写入。"
```

新 description：

```json
"钉钉 AI 表格（多维表）业务操作。Use when 用户需要操作 AI 表格/多维表/Base/Table、应用模式/App 页面/Widget、建表、查写记录、字段、记录评论、评论回复、访问密钥（API Key）、SQL/PostgreSQL/SELECT/JOIN、筛选、排序、公式、模板、批量导入 CSV 或 JSON、导出、仪表盘、图表、上传附件、数据源配置与同步、按任务 ID 查询同步状态或审批数据同步。普通请求以完成明确的业务操作为主；当用户明确要求 CLI 契约评审、核对 aitable 合成 JSON 回执、dry-run、命令参数、Help/Schema 契约或恢复方案时，必须加载本 Skill。只评审 aitable 合成 JSON 回执也必须加载本 Skill；“不要执行线上业务”不等于免除本机离线契约核对，不能按通用 JSON 经验直接作答。这是本机 Help/Schema 契约核对，不是仓库源码审查，不从源码搜索开始；先加载正文确定入口与规则，不能仅凭摘要执行；以用户原文指定的核对入口为准，Skill 参数不得扩大范围。不做电子表格单元格读写或单元格批注（走 dingtalk-misc）、文档编辑（走 dingtalk-doc）；听记待办入表先用 dingtalk-minutes 提取，再由本 skill 写入。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 11. dingtalk-calendar

- 入口文件：`/Users/zs/.agents/skills/dingtalk-calendar/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/dingtalk-calendar/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/dingtalk-calendar/agents/openai.yaml`

旧 description：

```json
"钉钉日历与会议室。Use when 用户说 约会议/查日程/订会议室/查闲忙/加参会人/改期/取消会议/今天的日程/本周日程/共同空闲。不做视频会议发起/邀请入会/会中控制（走 dingtalk-misc）、AI 听记（走 dingtalk-minutes）、待办任务（走 dingtalk-todo）。命令前缀：dws calendar。"
```

新 description：

```json
"钉钉日历与会议室。Use when 用户说 约会议/查日程/订会议室/查闲忙/加参会人/改期/取消会议/今天的日程/本周日程/共同空闲。不做视频会议发起/邀请入会/会中控制（走 dingtalk-misc）、AI 听记（走 dingtalk-minutes）、待办任务（走 dingtalk-todo）。命令前缀：dws calendar。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 12. dingtalk-chat

- 入口文件：`/Users/zs/.agents/skills/dingtalk-chat/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/dingtalk-chat/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/dingtalk-chat/agents/openai.yaml`

旧 description：

```json
"钉钉群聊与消息。Use when 收发/搜索消息、建群、群治理、Bot/Webhook、文件、AI/A2UI 卡片流式，或仅限 IM 的消息谓词筛选。跨源主题/行为轨迹走 dingtalk-aisearch；DING/班级群走 dingtalk-misc；邮件走 dingtalk-mail。"
```

新 description：

```json
"钉钉群聊与消息。Use when 收发/搜索消息、建群、群治理、Bot/Webhook、文件、AI/A2UI 卡片流式，或仅限 IM 的消息谓词筛选。跨源主题/行为轨迹走 dingtalk-aisearch；DING/班级群走 dingtalk-misc；邮件走 dingtalk-mail。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 13. dingtalk-contact

- 入口文件：`/Users/zs/.agents/skills/dingtalk-contact/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/dingtalk-contact/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/dingtalk-contact/agents/openai.yaml`

旧 description：

```json
"钉钉通讯录精确查询。Use when 已有 userId 后查详情、部门、职位或邮箱，按完整手机号反查用户，或查询自己、部门成员及角色。姓名模糊搜索、工号、职责、上下级走 dingtalk-aisearch，拿到 userId 后用本 skill 补详情。命令前缀：dws contact。"
```

新 description：

```json
"钉钉通讯录精确查询。Use when 已有 userId 后查详情、部门、职位或邮箱，按完整手机号反查用户，或查询自己、部门成员及角色。姓名模糊搜索、工号、职责、上下级走 dingtalk-aisearch，拿到 userId 后用本 skill 补详情。命令前缀：dws contact。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 14. dingtalk-doc

- 入口文件：`/Users/zs/.agents/skills/dingtalk-doc/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/dingtalk-doc/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/dingtalk-doc/agents/openai.yaml`

旧 description：

```json
"钉钉在线文档（adoc）：查找、读写、块、评论、附件、导入导出、版本、模板、权限、分享、Markdown/JSONML；文档内白板卡片容器的插入、定位、删除。白板图形内容创建或修改走 dingtalk-misc。"
```

新 description：

```json
"钉钉在线文档（adoc）：查找、读写、块、评论、附件、导入导出、版本、模板、权限、分享、Markdown/JSONML；文档内白板卡片容器的插入、定位、删除。白板图形内容创建或修改走 dingtalk-misc。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 15. dingtalk-drive

- 入口文件：`/Users/zs/.agents/skills/dingtalk-drive/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/dingtalk-drive/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/dingtalk-drive/agents/openai.yaml`

旧 description：

```json
"钉钉文件管理（存储层，覆盖钉盘与文档空间）。Use when 用户说 钉盘/文档空间/我的文档中的普通文件或文件夹、查找/最近访问或编辑文档列表/上传/下载/复制/移动/重命名/删除/回收站/权限/评论/元信息，或本地与钉盘文件夹比较、拉取、推送、双向同步；也承接在线文档节点的存储管理。文档正文编辑与导出走 dingtalk-doc；明确的知识库空间及空间内节点组织走 dingtalk-wiki。命令前缀：dws drive。"
```

新 description：

```json
"钉钉文件管理（存储层，覆盖钉盘与文档空间）。Use when 用户说 钉盘/文档空间/我的文档中的普通文件或文件夹、查找/最近访问或编辑文档列表/上传/下载/复制/移动/重命名/删除/回收站/权限/评论/元信息，或本地与钉盘文件夹比较、拉取、推送、双向同步；也承接在线文档节点的存储管理。文档正文编辑与导出走 dingtalk-doc；明确的知识库空间及空间内节点组织走 dingtalk-wiki。命令前缀：dws drive。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 16. dingtalk-event

- 入口文件：`/Users/zs/.agents/skills/dingtalk-event/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/dingtalk-event/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/dingtalk-event/agents/openai.yaml`

旧 description：

```json
"钉钉个人 IM、OA 审批、VoIP 通话邀请、待办、互动卡片与好友事件长连接监听。Use when 用户说监听消息/@我/某人/某群/全部消息、已读/撤回/reaction、群成员加入/群成员退出，监听审批任务创建/完成/转交、审批实例发起/抄送/终止/完成、VoIP 通话邀请、待办创建/更新/删除、好友申请/好友添加成功，或互动卡片回调。命令前缀：dws event。"
```

新 description：

```json
"钉钉个人 IM、OA 审批、VoIP 通话邀请、待办、互动卡片与好友事件长连接监听。Use when 用户说监听消息/@我/某人/某群/全部消息、已读/撤回/reaction、群成员加入/群成员退出，监听审批任务创建/完成/转交、审批实例发起/抄送/终止/完成、VoIP 通话邀请、待办创建/更新/删除、好友申请/好友添加成功，或互动卡片回调。命令前缀：dws event。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 17. dingtalk-mail

- 入口文件：`/Users/zs/.agents/skills/dingtalk-mail/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/dingtalk-mail/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/dingtalk-mail/agents/openai.yaml`

旧 description：

```json
"钉钉邮箱读写、搜索、回复与转发。Use when 用户说发邮件/查邮件/回邮件/转发邮件/未读邮件/邮件搜索/邮箱附件。一句话发邮件时先用 dingtalk-contact 解析并确认收件人，再由本 skill 发送；不做钉钉消息（走 dingtalk-chat）、紧急通知（走 dingtalk-misc）。命令前缀：dws mail。"
```

新 description：

```json
"钉钉邮箱读写、搜索、回复与转发。Use when 用户说发邮件/查邮件/回邮件/转发邮件/未读邮件/邮件搜索/邮箱附件。一句话发邮件时先用 dingtalk-contact 解析并确认收件人，再由本 skill 发送；不做钉钉消息（走 dingtalk-chat）、紧急通知（走 dingtalk-misc）。命令前缀：dws mail。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 18. dingtalk-minutes

- 入口文件：`/Users/zs/.agents/skills/dingtalk-minutes/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/dingtalk-minutes/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/dingtalk-minutes/agents/openai.yaml`

旧 description：

```json
"钉钉 AI 听记。Use when 查询或修改听记摘要、完整逐字稿、关键词、标签、行动项、录音、上传、思维导图、发言人洞察、ASR 热词/识别词配置或分享权限。写文档走 dingtalk-doc；建待办走 dingtalk-todo；日程走 dingtalk-calendar。命令前缀：dws minutes。"
```

新 description：

```json
"钉钉 AI 听记。Use when 查询或修改听记摘要、完整逐字稿、关键词、标签、行动项、录音、上传、思维导图、发言人洞察、ASR 热词/识别词配置或分享权限。写文档走 dingtalk-doc；建待办走 dingtalk-todo；日程走 dingtalk-calendar。命令前缀：dws minutes。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 19. dingtalk-misc

- 入口文件：`/Users/zs/.agents/skills/dingtalk-misc/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/dingtalk-misc/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/dingtalk-misc/agents/openai.yaml`

旧 description：

```json
"钉钉独立白板（白板文件）的创建、绘图、保存和修改；文档内嵌白板仅在已有承载文档 nodeId 和 partId 时提供图形内容读写（dws whiteboard）。两类目标相互独立，不互相推断或切换；文档内白板卡片容器不属于本 skill。长尾产品集合技能，覆盖低频钉钉产品：OA审批查询与处理/法务智能合同/考勤/直播/DING紧急消息/开放平台应用与MCP开发/Agoal目标管理/日志日报周报/电子表格/开放平台文档搜索与OpenAPI逃生舱/DWS技能市场安装/组织大脑Hrbrain/原生Markdown/原生HTML/PAT行为授权/多组织profile。Use when 用户提到上述任一产品，尤其是 Agoal/目标管理/战略解码/经营合约及字段配置/计分卡/OKR/目标规则与周期/个人目标/目标模板/周月报规则提交统计/按时/迟交/未提交/跟催，或查询/创建合同台账、批量导入合同、按听记起草合同、归档合同、管理合同项目/相对方/账款，或查待审批/同意拒绝转交撤销审批/打卡/排班/日报周报内容填报/独立白板带内容创建/独立白板节点读写/已有 nodeId 和 partId 的文档内嵌白板图形内容读写/单元格读写/搜索安装技能/开发者后台应用/企业内部应用/查应用状态或能否删除/应用管理成员及角色汇总/应用版本历史/企业内部应用机器人配置、消息模式或在线状态/本机机器人连接器/Stream连接/MCP服务或工具/发布或调试MCP/获取或调用已发布MCP/把OpenAPI、Swagger、Postman、curl或HTTP接口做成MCP或给Agent使用/未封装OpenAPI/llms.txt/dws api/人才池/员工档案/职业历程/绩效/原生.md文件/Markdown版本比较/本地草稿diff/Markdown评论/原生.html文件/新建HTML页面/PAT授权/切换组织/跨组织/profile 等相关操作。周报/月报内容填报属于 report；规则级按时、迟交、未提交统计与人员跟催属于 Agoal；带审批人、抄送人或审批流的日报、周报、简报提交属于 OA 审批。未来审批任务或实例变化的实时监听不属于本 skill，应使用 dingtalk-event。命中后由本 skill 的「产品索引表」定位具体子产品和命令前缀，再按对应子产品说明执行。"
```

新 description：

```json
"钉钉独立白板（白板文件）的创建、绘图、保存和修改；文档内嵌白板仅在已有承载文档 nodeId 和 partId 时提供图形内容读写（dws whiteboard）。两类目标相互独立，不互相推断或切换；文档内白板卡片容器不属于本 skill。长尾产品集合技能，覆盖低频钉钉产品：OA审批查询与处理/法务智能合同/考勤/直播/DING紧急消息/开放平台应用与MCP开发/Agoal目标管理/日志日报周报/电子表格/开放平台文档搜索与OpenAPI逃生舱/DWS技能市场安装/组织大脑Hrbrain/原生Markdown/原生HTML/PAT行为授权/多组织profile。Use when 用户提到上述任一产品，尤其是 Agoal/目标管理/战略解码/经营合约及字段配置/计分卡/OKR/目标规则与周期/个人目标/目标模板/周月报规则提交统计/按时/迟交/未提交/跟催，或查询/创建合同台账、批量导入合同、按听记起草合同、归档合同、管理合同项目/相对方/账款，或查待审批/同意拒绝转交撤销审批/打卡/排班/日报周报内容填报/独立白板带内容创建/独立白板节点读写/已有 nodeId 和 partId 的文档内嵌白板图形内容读写/单元格读写/搜索安装技能/开发者后台应用/企业内部应用/查应用状态或能否删除/应用管理成员及角色汇总/应用版本历史/企业内部应用机器人配置、消息模式或在线状态/本机机器人连接器/Stream连接/MCP服务或工具/发布或调试MCP/获取或调用已发布MCP/把OpenAPI、Swagger、Postman、curl或HTTP接口做成MCP或给Agent使用/未封装OpenAPI/llms.txt/dws api/人才池/员工档案/职业历程/绩效/原生.md文件/Markdown版本比较/本地草稿diff/Markdown评论/原生.html文件/新建HTML页面/PAT授权/切换组织/跨组织/profile 等相关操作。周报/月报内容填报属于 report；规则级按时、迟交、未提交统计与人员跟催属于 Agoal；带审批人、抄送人或审批流的日报、周报、简报提交属于 OA 审批。未来审批任务或实例变化的实时监听不属于本 skill，应使用 dingtalk-event。命中后由本 skill 的「产品索引表」定位具体子产品和命令前缀，再按对应子产品说明执行。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 20. dingtalk-shared

- 入口文件：`/Users/zs/.agents/skills/dingtalk-shared/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/dingtalk-shared/SKILL.md`

旧 description：

```json
"钉钉(DingTalk) MultiSkill 的轻量共享入口。Use when 用户泛称 DWS/钉钉操作但未明确产品、请求跨产品编排、需要 URL 类型预检或产品边界消歧。清晰的单产品操作优先使用对应 dingtalk-* 子 skill；本 skill 只提供全局执行契约和按需 reference 导航，不承载产品命令全集。"
```

新 description：

```json
"处理钉钉相关任务时用。不用于飞书、个人微信或纯本地文件操作。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": null
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": null
  }
}
```

## 21. dingtalk-tag

- 入口文件：`/Users/zs/.agents/skills/dingtalk-tag/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/dingtalk-tag/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/dingtalk-tag/agents/openai.yaml`

旧 description：

```json
"钉钉数字员工的自然语言创建、查询、修改、发布、删除、能力资源、执行状态、本地 Profile 落盘与 DSH 接入。Use when 用户说创建或管理数字员工、改人设/岗位/响应模式、发布或询问下线能力、查执行状态或 trace、管理数字员工 Skill/MCP、把已有数字员工转换为本地 Profile，或接入本地 DSH。命令前缀：dws dingtalk-tag。"
```

新 description：

```json
"钉钉数字员工的自然语言创建、查询、修改、发布、删除、能力资源、执行状态、本地 Profile 落盘与 DSH 接入。Use when 用户说创建或管理数字员工、改人设/岗位/响应模式、发布或询问下线能力、查执行状态或 trace、管理数字员工 Skill/MCP、把已有数字员工转换为本地 Profile，或接入本地 DSH。命令前缀：dws dingtalk-tag。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 22. dingtalk-todo

- 入口文件：`/Users/zs/.agents/skills/dingtalk-todo/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/dingtalk-todo/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/dingtalk-todo/agents/openai.yaml`

旧 description：

```json
"钉钉待办 / TODO。Use when 用户说 创建待办/TODO/任务提醒/指派任务/标记完成/查待办/紧急待办/循环待办/批量建待办/逾期待办。不做日报周报（走 dingtalk-misc）、审批（走 dingtalk-misc）、日程（走 dingtalk-calendar）。命令前缀：dws todo。"
```

新 description：

```json
"钉钉待办 / TODO。Use when 用户说 创建待办/TODO/任务提醒/指派任务/标记完成/查待办/紧急待办/循环待办/批量建待办/逾期待办。不做日报周报（走 dingtalk-misc）、审批（走 dingtalk-misc）、日程（走 dingtalk-calendar）。命令前缀：dws todo。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 23. dingtalk-wiki

- 入口文件：`/Users/zs/.agents/skills/dingtalk-wiki/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/dingtalk-wiki/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/dingtalk-wiki/agents/openai.yaml`

旧 description：

```json
"钉钉知识库与空间管理。Use when 用户明确说 知识库/wiki/创建、查找或列出知识库/命名的团队知识空间/个人知识库/知识库成员/库内节点创建、列表、搜索、复制、移动、删除或知识库动态。仅说“文档空间/我的文档”不触发：普通存储管理与全局文件搜索走 dingtalk-drive；节点正文读写走 dingtalk-doc。命令前缀：dws wiki。"
```

新 description：

```json
"钉钉知识库与空间管理。Use when 用户明确说 知识库/wiki/创建、查找或列出知识库/命名的团队知识空间/个人知识库/知识库成员/库内节点创建、列表、搜索、复制、移动、删除或知识库动态。仅说“文档空间/我的文档”不触发：普通存储管理与全局文件搜索走 dingtalk-drive；节点正文读写走 dingtalk-doc。命令前缀：dws wiki。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 24. doc-coauthoring

- 入口文件：`/Users/zs/.agents/skills/doc-coauthoring/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/doc-coauthoring/SKILL.md`

旧 description：

```json
"Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks."
```

新 description：

```json
"共同撰写方案或说明文档时用。不用于一般文章创作、单句润色或文件格式处理。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": null
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": null
  }
}
```

## 25. docx

- 入口文件：`/Users/zs/.agents/skills/docx/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/docx/SKILL.md`

旧 description：

```json
"Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation."
```

新 description：

```json
"创建或编辑 Word 文档时用。不用于纯文本草稿、表格文件或演示文稿。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": null
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": null
  }
}
```

## 26. embedded-captions

- 入口文件：`/Users/zs/.agents/skills/embedded-captions/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/embedded-captions/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/embedded-captions/agents/openai.yaml`

旧 description：

```json
"Add captions or subtitles to an existing single-subject talking-head video without editing the footage. Use for plain verbatim captions, cinematic captions embedded behind the subject, VFX captions, “炸/特效/酷炫字幕,” or a named identity from the 35-style catalog. Route by visual identity, not by backend engine. The quiet `anchor` rail is the default; embed every word only when the user explicitly wants a fully cinematic treatment. The workflow runs locally end to end, including transcription and subject matting; split multi-shot footage before applying it.\n"
```

新 description：

```json
"Add captions or subtitles to an existing single-subject talking-head video without editing the footage. Use for plain verbatim captions, cinematic captions embedded behind the subject, VFX captions, “炸/特效/酷炫字幕,” or a named identity from the 35-style catalog. Route by visual identity, not by backend engine. The quiet `anchor` rail is the default; embed every word only when the user explicitly wants a fully cinematic treatment. The workflow runs locally end to end, including transcription and subject matting; split multi-shot footage before applying it.\n"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 27. faceless-explainer

- 入口文件：`/Users/zs/.agents/skills/faceless-explainer/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/faceless-explainer/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/faceless-explainer/agents/openai.yaml`

旧 description：

```json
"Turn arbitrary text — an article, notes, a topic, a brief — into a faceless explainer video: there is no site or footage to capture, so the visuals are invented per scene (typography, abstract graphics, diagrams, data-viz). Use for topic explainers, concept breakdowns, how-tos, listicles. Not a video built from a website (/product-launch-video — promo or tour). Unclear → /hyperframes."
```

新 description：

```json
"Turn arbitrary text — an article, notes, a topic, a brief — into a faceless explainer video: there is no site or footage to capture, so the visuals are invented per scene (typography, abstract graphics, diagrams, data-viz). Use for topic explainers, concept breakdowns, how-tos, listicles. Not a video built from a website (/product-launch-video — promo or tour). Unclear → /hyperframes."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 28. figma

- 入口文件：`/Users/zs/.agents/skills/figma/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/figma/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/figma/agents/openai.yaml`

旧 description：

```json
"Bring Figma into a HyperFrames video - rendered assets, brand tokens, components, storyboard frames as reconstructed motion (frames read as states, not slides), shaders and connector-assisted motion. Use when the person pastes a figma.com link or asks to use a Figma design, frame, logo or brand."
```

新 description：

```json
"Bring Figma into a HyperFrames video - rendered assets, brand tokens, components, storyboard frames as reconstructed motion (frames read as states, not slides), shaders and connector-assisted motion. Use when the person pastes a figma.com link or asks to use a Figma design, frame, logo or brand."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 29. find-skills

- 入口文件：`/Users/zs/.agents/skills/find-skills/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/find-skills/SKILL.md`

旧 description：

```json
"Helps users discover and install agent skills when they ask questions like \"how do I do X\", \"find a skill for X\", \"is there a skill that can...\", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill."
```

新 description：

```json
"查找可安装的技能时用。不用于直接执行业务或修改现有技能内容。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": null
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": null
  }
}
```

## 30. frontend-design

- 入口文件：`/Users/zs/.agents/skills/frontend-design/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/frontend-design/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/frontend-design/agents/openai.yaml`

旧 description：

```json
"Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typography, and making choices that don't read as templated defaults."
```

新 description：

```json
"Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typography, and making choices that don't read as templated defaults."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 31. general-video

- 入口文件：`/Users/zs/.agents/skills/general-video/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/general-video/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/general-video/agents/openai.yaml`

旧 description：

```json
"Author or edit a custom HyperFrames composition when no specialized workflow fits, or when BRIEF.md sets flow: companion. Use for longer or multi-scene pieces, brand and sizzle reels, montages, static loops, static title cards, footage remixes, and freeform builds. Use motion-graphics instead for a short unnarrated motion-first unit, including an animated title. Route fresh creation through hyperframes before using this skill.\n"
```

新 description：

```json
"Author or edit a custom HyperFrames composition when no specialized workflow fits, or when BRIEF.md sets flow: companion. Use for longer or multi-scene pieces, brand and sizzle reels, montages, static loops, static title cards, footage remixes, and freeform builds. Use motion-graphics instead for a short unnarrated motion-first unit, including an animated title. Route fresh creation through hyperframes before using this skill.\n"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 32. guizang-social-card-skill

- 入口文件：`/Users/zs/.agents/skills/guizang-social-card-skill/SKILL.md`、`/Users/zs/.codex/skills/guizang-social-card-skill/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/guizang-social-card-skill/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/guizang-social-card-skill/agents/openai.yaml`

旧 description：

```json
"Generate Guizang-style social card image sets, Live Photo motion cards, material-first Live Photo puzzle layouts, triple Live Photo collages, long-video-to-Live-Photo treatments, and WeChat official account cover pairs from articles, scripts, screenshots, product notes, subtitles, photos, or user-supplied videos. Use when the user asks for 小红书图文, Rednote/Xiaohongshu images, social cards, carousel images, 3:4 covers, Live Photo, 实况照片, 单视频实况拼图, 二宫格实况拼图, 三连实况拼图, 四宫格实况拼图, 微信公众号封面, WeChat 21:9 + 1:1 covers, Swiss Style, or magazine-style social images."
```

新 description：

```json
"Generate Guizang-style social card image sets, Live Photo motion cards, material-first Live Photo puzzle layouts, triple Live Photo collages, long-video-to-Live-Photo treatments, and WeChat official account cover pairs from articles, scripts, screenshots, product notes, subtitles, photos, or user-supplied videos. Use when the user asks for 小红书图文, Rednote/Xiaohongshu images, social cards, carousel images, 3:4 covers, Live Photo, 实况照片, 单视频实况拼图, 二宫格实况拼图, 三连实况拼图, 四宫格实况拼图, 微信公众号封面, WeChat 21:9 + 1:1 covers, Swiss Style, or magazine-style social images."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": true,
    "after": false
  }
}
```

## 33. huashu-motion

- 入口文件：`/Users/zs/.agents/skills/huashu-motion/SKILL.md`、`/Users/zs/.codex/skills/huashu-motion/SKILL.md`
- 实际修改文件：`/Users/zs/.local/share/huashu-motion/skills/huashu-motion/SKILL.md`
- Codex 策略文件：`/Users/zs/.local/share/huashu-motion/skills/huashu-motion/agents/openai.yaml`

旧 description：

```json
"Motion graphics, launch videos and explainers as editable code. A director picks the motion language for your product; you point at frames to change them. 动画、发布片、解说视频，指着画面改。"
```

新 description：

```json
"Motion graphics, launch videos and explainers as editable code. A director picks the motion language for your product; you point at frames to change them. 动画、发布片、解说视频，指着画面改。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 34. humanize-ppt

- 入口文件：`/Users/zs/.agents/skills/humanize-ppt/SKILL.md`、`/Users/zs/.codex/skills/humanize-ppt/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/humanize-ppt/SKILL.md`

旧 description：

```json
"A presentation system for agent-made PPTs — born for the talk, not just the template. It turns raw material into an AST (audience-state-transfer) outline with per-page visual-enhancement decisions (image / SVG diagram / video), hands a production brief to a downstream renderer (HTML-PPT skills or native PPTX), then runs a capped 3-round presentation checkup (演讲体检) on the rendered deck. It never renders slides itself. Use before generating PPT/HTML slides from raw material, and after rendering when the user says things like \"给这份 deck 做演讲体检\" or \"PPT 渲染质检\". If all you want is one beautiful template page with no outline and no checkup, a rendering skill alone is enough."
```

新 description：

```json
"规划演示文稿或检查演讲效果时用。不用于单页模板美化或单纯渲染文件。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": null
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": null
  }
}
```

## 35. hyperframes

- 入口文件：`/Users/zs/.agents/skills/hyperframes/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/hyperframes/SKILL.md`

旧 description：

```json
"Read first to make, edit, animate or render any video with HyperFrames (HTML rendered to video), including launch films, explainers, music videos, charts, maps, vertical clips, title cards, captions and overlays. Holds the render contract, the work loop and what each kind of video needs."
```

新 description：

```json
"制作或编辑视频时用。不用于单张图片、纯文字稿或视频播放问题。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": null
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": null
  }
}
```

## 36. hyperframes-animation

- 入口文件：`/Users/zs/.agents/skills/hyperframes-animation/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/hyperframes-animation/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/hyperframes-animation/agents/openai.yaml`

旧 description：

```json
"All animation knowledge for HyperFrames — atomic motion rules, multi-phase scene blueprints, scene transitions, broader motion-design techniques, AND the seven runtime adapters (GSAP default, plus Lottie, Three.js, Anime.js, CSS keyframes, Web Animations API, TypeGPU). Use for any motion or animation task: pick 2-4 rules and compose, or load a blueprint, or look up runtime-specific API (e.g. GSAP eases / Lottie player / Three.js mixer). Also covers auditing an existing composition's choreography (animation map) and 24 named text-animation effects. HyperFrames-native: single paused timeline, seek-safe, deterministic."
```

新 description：

```json
"All animation knowledge for HyperFrames — atomic motion rules, multi-phase scene blueprints, scene transitions, broader motion-design techniques, AND the seven runtime adapters (GSAP default, plus Lottie, Three.js, Anime.js, CSS keyframes, Web Animations API, TypeGPU). Use for any motion or animation task: pick 2-4 rules and compose, or load a blueprint, or look up runtime-specific API (e.g. GSAP eases / Lottie player / Three.js mixer). Also covers auditing an existing composition's choreography (animation map) and 24 named text-animation effects. HyperFrames-native: single paused timeline, seek-safe, deterministic."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 37. hyperframes-audio

- 入口文件：`/Users/zs/.agents/skills/hyperframes-audio/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/hyperframes-audio/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/hyperframes-audio/agents/openai.yaml`

旧 description：

```json
"Use when audio already placed in a HyperFrames composition needs to be mixed: fade-in/fade-out, crossfade, track gain or volume, volume automation, ducking, a music bed that fights a voiceover (voiceover carve), effects on a track (EQ, compressor, limiter, gate, saturation, delay, reverb, chorus, phaser, bitcrush), automation envelopes drawn on a track's volume or any effect parameter, or one submix bus carrying a chain, a fader and an automation clock for several tracks at once (`<hf-audio-group>`). Don't use for sourcing or generating audio — finding BGM, SFX, or making a voiceover is `/media-use`. Don't use for clip timing or track layout, which is `/hyperframes-core`.\n"
```

新 description：

```json
"Use when audio already placed in a HyperFrames composition needs to be mixed: fade-in/fade-out, crossfade, track gain or volume, volume automation, ducking, a music bed that fights a voiceover (voiceover carve), effects on a track (EQ, compressor, limiter, gate, saturation, delay, reverb, chorus, phaser, bitcrush), automation envelopes drawn on a track's volume or any effect parameter, or one submix bus carrying a chain, a fader and an automation clock for several tracks at once (`<hf-audio-group>`). Don't use for sourcing or generating audio — finding BGM, SFX, or making a voiceover is `/media-use`. Don't use for clip timing or track layout, which is `/hyperframes-core`.\n"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 38. hyperframes-cli

- 入口文件：`/Users/zs/.agents/skills/hyperframes-cli/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/hyperframes-cli/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/hyperframes-cli/agents/openai.yaml`

旧 description：

```json
"The HyperFrames CLI by job - scaffold, check, look at frames, edit the timeline, preview, render locally or in the cloud, publish, project history - plus reading its JSON and recovering from build or render failures."
```

新 description：

```json
"The HyperFrames CLI by job - scaffold, check, look at frames, edit the timeline, preview, render locally or in the cloud, publish, project history - plus reading its JSON and recovering from build or render failures."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 39. hyperframes-core

- 入口文件：`/Users/zs/.agents/skills/hyperframes-core/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/hyperframes-core/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/hyperframes-core/agents/openai.yaml`

旧 description：

```json
"The HyperFrames composition contract — build one renderable project. Use for composition structure, the `data-*` timing attributes, `class=\"clip\"`, tracks, sub-compositions, variables, framework-owned media playback, deterministic-render rules, and validation. Read before writing composition HTML."
```

新 description：

```json
"The HyperFrames composition contract — build one renderable project. Use for composition structure, the `data-*` timing attributes, `class=\"clip\"`, tracks, sub-compositions, variables, framework-owned media playback, deterministic-render rules, and validation. Read before writing composition HTML."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 40. hyperframes-creative

- 入口文件：`/Users/zs/.agents/skills/hyperframes-creative/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/hyperframes-creative/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/hyperframes-creative/agents/openai.yaml`

旧 description：

```json
"Non-animation creative direction for HyperFrames videos. Use for design spec (frame.md / design.md) handling, palettes, typography, narration, beat planning, audio-reactive visuals, composition patterns, and brand / style decisions. For atomic motion patterns and scene blueprints, use `hyperframes-animation`."
```

新 description：

```json
"Non-animation creative direction for HyperFrames videos. Use for design spec (frame.md / design.md) handling, palettes, typography, narration, beat planning, audio-reactive visuals, composition patterns, and brand / style decisions. For atomic motion patterns and scene blueprints, use `hyperframes-animation`."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 41. hyperframes-keyframes

- 入口文件：`/Users/zs/.agents/skills/hyperframes-keyframes/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/hyperframes-keyframes/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/hyperframes-keyframes/agents/openai.yaml`

旧 description：

```json
"Use when a HyperFrames composition needs a punch-in, punch-out, zoom, reframe, Ken Burns treatment, camera move, visual match/whip handoff, or other seek-safe 2D/3D keyframes; also for GSAP, CSS keyframes, Anime.js, WAAPI, FLIP, paths, masks, SVG morph/draw, text trails, 3D depth, or `hyperframes keyframes` diagnostics. Don't use for broad scene strategy, brand design, media sourcing, captions, or general video planning.\n"
```

新 description：

```json
"Use when a HyperFrames composition needs a punch-in, punch-out, zoom, reframe, Ken Burns treatment, camera move, visual match/whip handoff, or other seek-safe 2D/3D keyframes; also for GSAP, CSS keyframes, Anime.js, WAAPI, FLIP, paths, masks, SVG morph/draw, text trails, 3D depth, or `hyperframes keyframes` diagnostics. Don't use for broad scene strategy, brand design, media sourcing, captions, or general video planning.\n"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 42. hyperframes-registry

- 入口文件：`/Users/zs/.agents/skills/hyperframes-registry/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/hyperframes-registry/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/hyperframes-registry/agents/openai.yaml`

旧 description：

```json
"About 450 ready-made HyperFrames blocks and components installed as editable source - transitions, overlays, titles, kinetic type, captions, charts, map overlays, 3D, camera moves. Use it before hand-building any named visual (CRT scanlines, glitch, film grain, a chart); also for hyperframes add and catalog."
```

新 description：

```json
"About 450 ready-made HyperFrames blocks and components installed as editable source - transitions, overlays, titles, kinetic type, captions, charts, map overlays, 3D, camera moves. Use it before hand-building any named visual (CRT scanlines, glitch, film grain, a chart); also for hyperframes add and catalog."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 43. image-story-video-wizard

- 入口文件：`/Users/zs/.agents/skills/image-story-video-wizard/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/image-story-video-wizard/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/image-story-video-wizard/agents/openai.yaml`

旧 description：

```json
"Use when a user wants step-by-step help making an audio-first image-story, AI narration, slideshow, illustrated story, AI 讲书, 图片联播, 有声故事, or 静态图叙事视频 with Codex or WorkBuddy; not for a standalone script, single image, or ordinary video editing."
```

新 description：

```json
"Use when a user wants step-by-step help making an audio-first image-story, AI narration, slideshow, illustrated story, AI 讲书, 图片联播, 有声故事, or 静态图叙事视频 with Codex or WorkBuddy; not for a standalone script, single image, or ordinary video editing."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": true,
    "after": false
  }
}
```

## 44. lark-approval

- 入口文件：`/Users/zs/.agents/skills/lark-approval/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-approval/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-approval/agents/openai.yaml`

旧 description：

```json
"飞书审批：查询和处理审批待办/已办/实例，搜索可发起审批定义、查看定义详情并发起原生审批实例。当用户要处理审批任务、查看审批实例、搜索或发起审批时使用。审批待办不是飞书任务；非审批类待办走 lark-task。不负责创建审批定义；三方审批定义不走原生提单。"
```

新 description：

```json
"飞书审批：查询和处理审批待办/已办/实例，搜索可发起审批定义、查看定义详情并发起原生审批实例。当用户要处理审批任务、查看审批实例、搜索或发起审批时使用。审批待办不是飞书任务；非审批类待办走 lark-task。不负责创建审批定义；三方审批定义不走原生提单。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 45. lark-apps

- 入口文件：`/Users/zs/.agents/skills/lark-apps/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-apps/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-apps/agents/openai.yaml`

旧 description：

```json
"妙搭（Spark/Miaoda）应用开发与托管：应用创建、本地全栈开发、云端生成迭代、创意设计（UI mockup / 可交互原型 / 线框图 / 落地页 / 仪表盘 / 幻灯片 deck / 视觉探索）、AI相关能力和飞书平台能力或者其他外部能力集成、日志/Trace/监控指标/PV/UV 查询、环境变量管理、应用协作者与协作权限设置、应用角色与成员管理、自动化触发器（定时/记录变更/Webhook/飞书审批）。当用户要开发/新建一个系统·工具·平台·应用，或要本地开发 / 云端开发 / 修改 / 部署 / 发布 / 上线 / 拿可分享链接，或用 HTML 做页面·网站·部署到妙搭，或要设计 / design / mockup / prototype / wireframe / 做 PPT / deck / 视觉探索，或提到妙搭/Spark/Miaoda（应用运行时域名形如 *.aiforce.cloud）、应用数据库、应用文件存储、开放 API Key、可见范围、应用协作者/开发权限、应用角色/角色成员、线上日志、接口请求量、错误量、延迟、访问量、环境变量、给妙搭应用配自动化任务/定时触发/审批通过后自动触发时使用。不负责普通云盘文件上传（lark-drive）、飞书文档编辑（lark-doc）、原生幻灯片创建（lark-slides）。"
```

新 description：

```json
"妙搭（Spark/Miaoda）应用开发与托管：应用创建、本地全栈开发、云端生成迭代、创意设计（UI mockup / 可交互原型 / 线框图 / 落地页 / 仪表盘 / 幻灯片 deck / 视觉探索）、AI相关能力和飞书平台能力或者其他外部能力集成、日志/Trace/监控指标/PV/UV 查询、环境变量管理、应用协作者与协作权限设置、应用角色与成员管理、自动化触发器（定时/记录变更/Webhook/飞书审批）。当用户要开发/新建一个系统·工具·平台·应用，或要本地开发 / 云端开发 / 修改 / 部署 / 发布 / 上线 / 拿可分享链接，或用 HTML 做页面·网站·部署到妙搭，或要设计 / design / mockup / prototype / wireframe / 做 PPT / deck / 视觉探索，或提到妙搭/Spark/Miaoda（应用运行时域名形如 *.aiforce.cloud）、应用数据库、应用文件存储、开放 API Key、可见范围、应用协作者/开发权限、应用角色/角色成员、线上日志、接口请求量、错误量、延迟、访问量、环境变量、给妙搭应用配自动化任务/定时触发/审批通过后自动触发时使用。不负责普通云盘文件上传（lark-drive）、飞书文档编辑（lark-doc）、原生幻灯片创建（lark-slides）。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 46. lark-attendance

- 入口文件：`/Users/zs/.agents/skills/lark-attendance/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-attendance/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-attendance/agents/openai.yaml`

旧 description：

```json
"飞书考勤打卡：查询自己的考勤打卡记录"
```

新 description：

```json
"飞书考勤打卡：查询自己的考勤打卡记录"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 47. lark-base

- 入口文件：`/Users/zs/.agents/skills/lark-base/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-base/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-base/agents/openai.yaml`

旧 description：

```json
"飞书多维表格（Base）操作：建表、字段、记录、视图、统计、公式/lookup、表单、仪表盘、应用模式（BaseApp/AppMode 页面与组件）、Workspace 目录、workflow、角色权限、模板中心（多维表格模板分类/列表/搜索）；遇到 Base/多维表格/bitable、BaseApp/AppMode、/base/ 或 /app/ 链接时使用。BaseApp 不走 lark-apps；文件导入/导出转 lark-drive，认证/授权转 lark-shared。"
```

新 description：

```json
"飞书多维表格（Base）操作：建表、字段、记录、视图、统计、公式/lookup、表单、仪表盘、应用模式（BaseApp/AppMode 页面与组件）、Workspace 目录、workflow、角色权限、模板中心（多维表格模板分类/列表/搜索）；遇到 Base/多维表格/bitable、BaseApp/AppMode、/base/ 或 /app/ 链接时使用。BaseApp 不走 lark-apps；文件导入/导出转 lark-drive，认证/授权转 lark-shared。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 48. lark-calendar

- 入口文件：`/Users/zs/.agents/skills/lark-calendar/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-calendar/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-calendar/agents/openai.yaml`

旧 description：

```json
"飞书日历：管理日历日程和会议室。查看/搜索日程、创建/更新日程、管理参会人、查询忙闲和推荐时段、预定会议室。当用户需要查看日程安排、创建/修改会议、查询/预定会议室时使用。不负责：查询过去的视频会议记录（走 lark-meeting）、待办任务（走 lark-task）。"
```

新 description：

```json
"飞书日历：管理日历日程和会议室。查看/搜索日程、创建/更新日程、管理参会人、查询忙闲和推荐时段、预定会议室。当用户需要查看日程安排、创建/修改会议、查询/预定会议室时使用。不负责：查询过去的视频会议记录（走 lark-meeting）、待办任务（走 lark-task）。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 49. lark-contact

- 入口文件：`/Users/zs/.agents/skills/lark-contact/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-contact/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-contact/agents/openai.yaml`

旧 description：

```json
"飞书 / Lark 通讯录:按姓名 / 邮箱解析成 open_id,或按 open_id 反查姓名 / 部门 / 邮箱 / 联系方式 / 个人状态 / 签名,以及按关键词搜索当前用户可见的机器人 / 智能体(agent)。当用户提到一个名字要下一步发消息 / 排日程,或拿到 open_id 想查具体信息时使用。不负责部门树遍历、按部门列员工、组织架构图,这类需求走原生 OpenAPI。"
```

新 description：

```json
"飞书 / Lark 通讯录:按姓名 / 邮箱解析成 open_id,或按 open_id 反查姓名 / 部门 / 邮箱 / 联系方式 / 个人状态 / 签名,以及按关键词搜索当前用户可见的机器人 / 智能体(agent)。当用户提到一个名字要下一步发消息 / 排日程,或拿到 open_id 想查具体信息时使用。不负责部门树遍历、按部门列员工、组织架构图,这类需求走原生 OpenAPI。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 50. lark-doc

- 入口文件：`/Users/zs/.agents/skills/lark-doc/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-doc/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-doc/agents/openai.yaml`

旧 description：

```json
"飞书云文档（Docx / Wiki）内容操作：读取、创建、编辑文档，插入或下载图片附件，以及操作思维笔记。用户提供文档 URL/token（包括 doubao.com 的 /docx/、/wiki/）时使用；按 URL 路径/token 而非域名路由。文档内嵌资源按读取参考中的统一规则分流。独立评论操作走 lark-drive；随正文读取评论使用 docs +fetch。表格或 Base 内部数据操作不在本 skill。"
```

新 description：

```json
"飞书云文档（Docx / Wiki）内容操作：读取、创建、编辑文档，插入或下载图片附件，以及操作思维笔记。用户提供文档 URL/token（包括 doubao.com 的 /docx/、/wiki/）时使用；按 URL 路径/token 而非域名路由。文档内嵌资源按读取参考中的统一规则分流。独立评论操作走 lark-drive；随正文读取评论使用 docs +fetch。表格或 Base 内部数据操作不在本 skill。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 51. lark-drive

- 入口文件：`/Users/zs/.agents/skills/lark-drive/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-drive/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-drive/agents/openai.yaml`

旧 description：

```json
"飞书云空间（云盘/云存储）：管理 Drive 文件和文件夹，包含上传/下载、创建文件夹、复制/移动/删除、查看元数据、查询权限设置、评论/权限/订阅、标题、版本、飞书文档密级标签（secure labels）和本地文件导入。用户需要整理云盘目录、处理云空间资源 URL/token、判断链接类型/真实 token/标题，或导入 Word/Markdown/Excel/CSV/PPTX/.base 为 docx/sheet/bitable/slides 时使用；doubao.com 云空间 URL/token 也按资源路径和 token 路由，不回退 WebFetch。不负责：文档内容编辑（走 lark-doc）、表格/Base 表内数据操作（走 lark-sheets/lark-base）、知识空间节点/成员管理（走 lark-wiki）、原生 Markdown 文件读写/patch/diff（走 lark-markdown）。"
```

新 description：

```json
"飞书云空间（云盘/云存储）：管理 Drive 文件和文件夹，包含上传/下载、创建文件夹、复制/移动/删除、查看元数据、查询权限设置、评论/权限/订阅、标题、版本、飞书文档密级标签（secure labels）和本地文件导入。用户需要整理云盘目录、处理云空间资源 URL/token、判断链接类型/真实 token/标题，或导入 Word/Markdown/Excel/CSV/PPTX/.base 为 docx/sheet/bitable/slides 时使用；doubao.com 云空间 URL/token 也按资源路径和 token 路由，不回退 WebFetch。不负责：文档内容编辑（走 lark-doc）、表格/Base 表内数据操作（走 lark-sheets/lark-base）、知识空间节点/成员管理（走 lark-wiki）、原生 Markdown 文件读写/patch/diff（走 lark-markdown）。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 52. lark-event

- 入口文件：`/Users/zs/.agents/skills/lark-event/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-event/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-event/agents/openai.yaml`

旧 description：

```json
"Lark/Feishu real-time event listening / subscribing / consuming: stream events as NDJSON via `lark-cli event consume <EventKey>` (covers IM messages/reactions/chat changes, Approval status changes, Task updates, VC meeting started/joined/ended, Minutes generated, Whiteboard updated, etc.). Use for Lark bots, real-time message processing, long-running subscribers, streaming webhook/push handlers. Supports `--max-events` / `--timeout` bounded runs and a stderr ready-marker contract — designed for AI agents running as subprocesses."
```

新 description：

```json
"Lark/Feishu real-time event listening / subscribing / consuming: stream events as NDJSON via `lark-cli event consume <EventKey>` (covers IM messages/reactions/chat changes, Approval status changes, Task updates, VC meeting started/joined/ended, Minutes generated, Whiteboard updated, etc.). Use for Lark bots, real-time message processing, long-running subscribers, streaming webhook/push handlers. Supports `--max-events` / `--timeout` bounded runs and a stderr ready-marker contract — designed for AI agents running as subprocesses."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 53. lark-im

- 入口文件：`/Users/zs/.agents/skills/lark-im/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-im/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-im/agents/openai.yaml`

旧 description：

```json
"飞书即时通讯：收发消息和管理群聊。发送和回复消息、搜索聊天记录、管理群聊成员、上传下载图片和文件、管理表情回复、发送应用内/短信/电话加急、发送和处理交互卡片（Interactive Card）、监听卡片按钮回调（card.action.trigger）。当用户需要发消息、查看或搜索聊天记录、下载聊天中的文件、查看群成员、搜索群、创建群聊或话题群、管理标记数据、管理 Feed 置顶（添加/移除/查询置顶会话）、管理标签数据、处理卡片回调时使用。"
```

新 description：

```json
"飞书即时通讯：收发消息和管理群聊。发送和回复消息、搜索聊天记录、管理群聊成员、上传下载图片和文件、管理表情回复、发送应用内/短信/电话加急、发送和处理交互卡片（Interactive Card）、监听卡片按钮回调（card.action.trigger）。当用户需要发消息、查看或搜索聊天记录、下载聊天中的文件、查看群成员、搜索群、创建群聊或话题群、管理标记数据、管理 Feed 置顶（添加/移除/查询置顶会话）、管理标签数据、处理卡片回调时使用。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 54. lark-mail

- 入口文件：`/Users/zs/.agents/skills/lark-mail/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-mail/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-mail/agents/openai.yaml`

旧 description：

```json
"飞书邮箱：Use when user mentions 起草邮件、写邮件、草稿、发送/回复/转发邮件、查阅邮件、看邮件、搜索邮件、邮件文件夹、邮件标签、邮件联系人、监听新邮件、邮件收信规则等；use for mail/email intent only. Do not use for docs/sheets/calendar/auth setup/pure contact lookup/IM chat tasks."
```

新 description：

```json
"飞书邮箱：Use when user mentions 起草邮件、写邮件、草稿、发送/回复/转发邮件、查阅邮件、看邮件、搜索邮件、邮件文件夹、邮件标签、邮件联系人、监听新邮件、邮件收信规则等；use for mail/email intent only. Do not use for docs/sheets/calendar/auth setup/pure contact lookup/IM chat tasks."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 55. lark-markdown

- 入口文件：`/Users/zs/.agents/skills/lark-markdown/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-markdown/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-markdown/agents/openai.yaml`

旧 description：

```json
"飞书 Markdown：查看、创建、上传、编辑和比较飞书中的原生 Markdown 文件。当用户要操作飞书 Markdown 文件，或比较其远端版本及本地草稿时使用。纯本地 Markdown 文件操作不触发本 skill。不负责将 Markdown 导入为飞书在线文档，也不负责文件搜索、权限、评论、移动、删除等云空间管理操作。"
```

新 description：

```json
"飞书 Markdown：查看、创建、上传、编辑和比较飞书中的原生 Markdown 文件。当用户要操作飞书 Markdown 文件，或比较其远端版本及本地草稿时使用。纯本地 Markdown 文件操作不触发本 skill。不负责将 Markdown 导入为飞书在线文档，也不负责文件搜索、权限、评论、移动、删除等云空间管理操作。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 56. lark-meeting

- 入口文件：`/Users/zs/.agents/skills/lark-meeting/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-meeting/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-meeting/agents/openai.yaml`

旧 description：

```json
"飞书视频会议：查询会议记录与会议产物(纪要/逐字稿/妙记)、妙记搜索/上传/下载/编辑、机器人参与会议；查询进行中的会议、实时会议内容(发言/聊天/共享文档)问答(会上/会里)、发送会中聊天/表情；基于 meeting_id、meeting_no、event_id、note_id、minute_token、vc-node-id 或妙记 URL 查询相关信息。预约会议、忙闲和会议室管理走 lark-calendar。"
```

新 description：

```json
"飞书视频会议：查询会议记录与会议产物(纪要/逐字稿/妙记)、妙记搜索/上传/下载/编辑、机器人参与会议；查询进行中的会议、实时会议内容(发言/聊天/共享文档)问答(会上/会里)、发送会中聊天/表情；基于 meeting_id、meeting_no、event_id、note_id、minute_token、vc-node-id 或妙记 URL 查询相关信息。预约会议、忙闲和会议室管理走 lark-calendar。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 57. lark-minutes

- 入口文件：`/Users/zs/.agents/skills/lark-minutes/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-minutes/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-minutes/agents/openai.yaml`

旧 description：

```json
"仅当用户或上游配置显式指定 lark-minutes 时使用，相关请求统一交由 lark-meeting 技能处理。"
```

新 description：

```json
"仅当用户或上游配置显式指定 lark-minutes 时使用，相关请求统一交由 lark-meeting 技能处理。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 58. lark-note

- 入口文件：`/Users/zs/.agents/skills/lark-note/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-note/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-note/agents/openai.yaml`

旧 description：

```json
"仅当用户或上游配置显式指定 lark-note 时使用，相关请求统一交由 lark-meeting 技能处理。"
```

新 description：

```json
"仅当用户或上游配置显式指定 lark-note 时使用，相关请求统一交由 lark-meeting 技能处理。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 59. lark-okr

- 入口文件：`/Users/zs/.agents/skills/lark-okr/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-okr/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-okr/agents/openai.yaml`

旧 description：

```json
"飞书 OKR：管理目标与关键结果。查看和编辑 OKR 周期、目标、关键结果、对齐关系、量化指标和进展记录。当用户需要查看或创建 OKR、管理目标和关键结果、查看对齐关系时使用。不负责：待办任务管理（lark-task）、日程/会议安排（lark-calendar）、绩效评估"
```

新 description：

```json
"飞书 OKR：管理目标与关键结果。查看和编辑 OKR 周期、目标、关键结果、对齐关系、量化指标和进展记录。当用户需要查看或创建 OKR、管理目标和关键结果、查看对齐关系时使用。不负责：待办任务管理（lark-task）、日程/会议安排（lark-calendar）、绩效评估"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 60. lark-openapi-explorer

- 入口文件：`/Users/zs/.agents/skills/lark-openapi-explorer/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-openapi-explorer/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-openapi-explorer/agents/openai.yaml`

旧 description：

```json
"飞书/Lark 原生 OpenAPI 探索：从官方文档库中挖掘未经 CLI 封装的原生 OpenAPI 接口。当用户的需求无法被现有 lark-* skill 或 lark-cli 已注册命令满足，需要查找并调用原生飞书 OpenAPI 时使用。"
```

新 description：

```json
"飞书/Lark 原生 OpenAPI 探索：从官方文档库中挖掘未经 CLI 封装的原生 OpenAPI 接口。当用户的需求无法被现有 lark-* skill 或 lark-cli 已注册命令满足，需要查找并调用原生飞书 OpenAPI 时使用。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 61. lark-shared

- 入口文件：`/Users/zs/.agents/skills/lark-shared/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-shared/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-shared/agents/openai.yaml`

旧 description：

```json
"Use for lark-cli setup/auth tasks: auth login/status/logout, user vs bot identity, business-domain permissions (--domain, including all/docs/drive), missing scopes, revoking authorization, or handling _notice JSON."
```

新 description：

```json
"Use for lark-cli setup/auth tasks: auth login/status/logout, user vs bot identity, business-domain permissions (--domain, including all/docs/drive), missing scopes, revoking authorization, or handling _notice JSON."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 62. lark-sheets

- 入口文件：`/Users/zs/.agents/skills/lark-sheets/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-sheets/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-sheets/agents/openai.yaml`

旧 description：

```json
"飞书电子表格：创建和操作电子表格。支持工作表与行列结构（增删/合并/尺寸/隐藏/冻结/分组）、单元格读写（值/公式/样式/批注/单元格图片）、区域复制移动排序填充、查找替换、批量更新，图表、透视表、条件格式、筛选器与筛选视图、下拉列表、迷你图、浮动图片等对象的创建与维护，以及公式校验、历史版本回滚、本地 Excel/CSV 与飞书表格的导入导出。当用户需要创建或编辑表格、统计汇总与可视化、表格美化、公式计算（含 Excel 公式迁移）、金融/财务建模（DCF、三张表、预算、Sensitivity 等）时使用。多维表格（Base/bitable）请改用 lark-base；若用户是想按名称或关键词搜索云空间（云盘/云存储）里的表格文件，请改用 lark-drive 的 drive +search 先定位资源。当用户给出 doubao.com 的 /sheets/ URL/token 时，也应直接使用本 skill，不要因为域名不是飞书而回退到 WebFetch；路由依据是 URL 路径模式和 token，而不是域名。"
```

新 description：

```json
"飞书电子表格：创建和操作电子表格。支持工作表与行列结构（增删/合并/尺寸/隐藏/冻结/分组）、单元格读写（值/公式/样式/批注/单元格图片）、区域复制移动排序填充、查找替换、批量更新，图表、透视表、条件格式、筛选器与筛选视图、下拉列表、迷你图、浮动图片等对象的创建与维护，以及公式校验、历史版本回滚、本地 Excel/CSV 与飞书表格的导入导出。当用户需要创建或编辑表格、统计汇总与可视化、表格美化、公式计算（含 Excel 公式迁移）、金融/财务建模（DCF、三张表、预算、Sensitivity 等）时使用。多维表格（Base/bitable）请改用 lark-base；若用户是想按名称或关键词搜索云空间（云盘/云存储）里的表格文件，请改用 lark-drive 的 drive +search 先定位资源。当用户给出 doubao.com 的 /sheets/ URL/token 时，也应直接使用本 skill，不要因为域名不是飞书而回退到 WebFetch；路由依据是 URL 路径模式和 token，而不是域名。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 63. lark-skill-maker

- 入口文件：`/Users/zs/.agents/skills/lark-skill-maker/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-skill-maker/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-skill-maker/agents/openai.yaml`

旧 description：

```json
"创建 lark-cli 的自定义 Skill。当用户需要把飞书 API 操作封装成可复用的 Skill（包装原子 API 或编排多步流程）时使用。"
```

新 description：

```json
"创建 lark-cli 的自定义 Skill。当用户需要把飞书 API 操作封装成可复用的 Skill（包装原子 API 或编排多步流程）时使用。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 64. lark-slides

- 入口文件：`/Users/zs/.agents/skills/lark-slides/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-slides/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-slides/agents/openai.yaml`

旧 description：

```json
"飞书幻灯片：创建和编辑幻灯片。创建演示文稿、读取幻灯片内容、管理幻灯片页面（创建、删除、读取、局部替换）。当用户需要创建或编辑幻灯片、读取或修改单个页面时使用。当用户给出 doubao.com 的 /slides/ URL/token 时，也应直接使用本 skill，不要因为域名不是飞书而回退到 WebFetch；路由依据是 URL 路径模式和 token，而不是域名。不负责：云文档内容编辑（走 lark-doc）、云文档里的独立画板对象（走 lark-whiteboard）、上传或下载普通文件（走 lark-drive）。"
```

新 description：

```json
"飞书幻灯片：创建和编辑幻灯片。创建演示文稿、读取幻灯片内容、管理幻灯片页面（创建、删除、读取、局部替换）。当用户需要创建或编辑幻灯片、读取或修改单个页面时使用。当用户给出 doubao.com 的 /slides/ URL/token 时，也应直接使用本 skill，不要因为域名不是飞书而回退到 WebFetch；路由依据是 URL 路径模式和 token，而不是域名。不负责：云文档内容编辑（走 lark-doc）、云文档里的独立画板对象（走 lark-whiteboard）、上传或下载普通文件（走 lark-drive）。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 65. lark-task

- 入口文件：`/Users/zs/.agents/skills/lark-task/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-task/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-task/agents/openai.yaml`

旧 description：

```json
"飞书任务：管理任务、清单和任务智能体。创建待办任务、查看和更新任务状态、拆分子任务、组织任务清单、分配协作成员、上传任务附件、注册或注销任务智能体、更新任务智能体的主页数据、写入智能体任务记录。当用户需要创建待办事项、查看任务列表、跟踪任务进度、管理项目清单或给他人分配任务、为任务上传附件文件、注册注销任务智能体、更新智能体主页数据、写入任务记录时使用。"
```

新 description：

```json
"飞书任务：管理任务、清单和任务智能体。创建待办任务、查看和更新任务状态、拆分子任务、组织任务清单、分配协作成员、上传任务附件、注册或注销任务智能体、更新任务智能体的主页数据、写入智能体任务记录。当用户需要创建待办事项、查看任务列表、跟踪任务进度、管理项目清单或给他人分配任务、为任务上传附件文件、注册注销任务智能体、更新智能体主页数据、写入任务记录时使用。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 66. lark-vc

- 入口文件：`/Users/zs/.agents/skills/lark-vc/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-vc/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-vc/agents/openai.yaml`

旧 description：

```json
"仅当用户或上游配置显式指定 lark-vc 时使用，相关请求统一交由 lark-meeting 技能处理。"
```

新 description：

```json
"仅当用户或上游配置显式指定 lark-vc 时使用，相关请求统一交由 lark-meeting 技能处理。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 67. lark-vc-agent

- 入口文件：`/Users/zs/.agents/skills/lark-vc-agent/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-vc-agent/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-vc-agent/agents/openai.yaml`

旧 description：

```json
"仅当用户或上游配置显式指定 lark-vc-agent 时使用，相关请求统一交由 lark-meeting 技能处理。"
```

新 description：

```json
"仅当用户或上游配置显式指定 lark-vc-agent 时使用，相关请求统一交由 lark-meeting 技能处理。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 68. lark-whiteboard

- 入口文件：`/Users/zs/.agents/skills/lark-whiteboard/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-whiteboard/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-whiteboard/agents/openai.yaml`

旧 description：

```json
"飞书画板：查询和编辑飞书云文档中的画板。支持导出画板为预览图片、导出原始节点结构、使用多种格式更新画板内容。 当用户需要查看画板内容、导出画板图片、编辑画板时使用此 skill。不负责：飞书云文档内容编辑（lark-doc）、文档内嵌电子表格/Base（lark-sheets / lark-base）。\n"
```

新 description：

```json
"飞书画板：查询和编辑飞书云文档中的画板。支持导出画板为预览图片、导出原始节点结构、使用多种格式更新画板内容。 当用户需要查看画板内容、导出画板图片、编辑画板时使用此 skill。不负责：飞书云文档内容编辑（lark-doc）、文档内嵌电子表格/Base（lark-sheets / lark-base）。\n"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 69. lark-wiki

- 入口文件：`/Users/zs/.agents/skills/lark-wiki/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-wiki/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-wiki/agents/openai.yaml`

旧 description：

```json
"飞书知识库：管理知识空间、空间成员和文档节点。创建和查询知识空间、查看和管理空间成员、管理节点层级结构、在知识库中组织文档和快捷方式。当用户需要在知识库中查找或创建文档、浏览知识空间结构、查看或管理空间成员、移动或复制节点时使用。当用户给出 doubao.com 的 /wiki/ URL/token 时，也应直接使用本 skill，不要因为域名不是飞书而回退到 WebFetch；路由依据是 URL 路径模式和 token，而不是域名。不负责：上传文件到知识库节点下（走 lark-drive）、编辑文档/表格/Base 内容（走 lark-doc / lark-sheets / lark-base）。"
```

新 description：

```json
"飞书知识库：管理知识空间、空间成员和文档节点。创建和查询知识空间、查看和管理空间成员、管理节点层级结构、在知识库中组织文档和快捷方式。当用户需要在知识库中查找或创建文档、浏览知识空间结构、查看或管理空间成员、移动或复制节点时使用。当用户给出 doubao.com 的 /wiki/ URL/token 时，也应直接使用本 skill，不要因为域名不是飞书而回退到 WebFetch；路由依据是 URL 路径模式和 token，而不是域名。不负责：上传文件到知识库节点下（走 lark-drive）、编辑文档/表格/Base 内容（走 lark-doc / lark-sheets / lark-base）。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 70. lark-workflow-meeting-summary

- 入口文件：`/Users/zs/.agents/skills/lark-workflow-meeting-summary/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-workflow-meeting-summary/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-workflow-meeting-summary/agents/openai.yaml`

旧 description：

```json
"会议纪要整理工作流：汇总指定时间范围内的会议纪要并生成结构化报告。当用户需要整理会议纪要、生成会议周报、回顾一段时间内的会议内容时使用。"
```

新 description：

```json
"会议纪要整理工作流：汇总指定时间范围内的会议纪要并生成结构化报告。当用户需要整理会议纪要、生成会议周报、回顾一段时间内的会议内容时使用。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 71. lark-workflow-standup-report

- 入口文件：`/Users/zs/.agents/skills/lark-workflow-standup-report/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lark-workflow-standup-report/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lark-workflow-standup-report/agents/openai.yaml`

旧 description：

```json
"日程待办摘要：编排 calendar +agenda 和 task +get-my-tasks，生成指定日期的日程与未完成任务摘要。适用于了解今天/明天/本周的安排。"
```

新 description：

```json
"日程待办摘要：编排 calendar +agenda 和 task +get-my-tasks，生成指定日期的日程与未完成任务摘要。适用于了解今天/明天/本周的安排。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 72. legacy-claude-context

- 入口文件：`/Users/zs/.agents/skills/legacy-claude-context/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/legacy-claude-context/SKILL.md`

旧 description：

```json
"Access durable memories, preferences, prior decisions, branches, deployments, QA findings, content-writing habits, and personal project context migrated from Claude Code. Use when the user refers to previous work or established habits, asks to continue a task started in Claude Code, works in GoalfyAI, asks about prior technical or product decisions, GitHub profile preferences, publishing workflows, or expects context that may have been learned in an earlier Claude session."
```

新 description：

```json
"查找 Claude 旧任务或偏好时用。不用于证明当前代码、部署或账号状态。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": null
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": null
  }
}
```

## 73. lemo-opuscar

- 入口文件：`/Users/zs/.agents/skills/lemo-opuscar/SKILL.md`、`/Users/zs/.codex/skills/lemo-opuscar/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/lemo-opuscar/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/lemo-opuscar/agents/openai.yaml`

旧 description：

```json
"Direct and produce a short film made entirely in code, in one of the styles of the Lemo-Opuscar library (e.g. Impasto Oil Painting 油画厚涂, Watercolor Brush 水彩笔刷, Ukiyo-e 浮世绘, Satellite Briefing 卫星简报, Exploded Teardown 产品拆解, Microscope Story 显微叙事). Use when the user asks for a video, film, short, promo, explainer or animation (视频、短片、动画、宣传片) in a named style, including data, science and product explainers built from real material such as satellite imagery, laser scans, CAD files or archive scans (数据解说、科普、产品拆解); when they want a film made about their own topic and haven't chosen a style (help them choose); or when they ask which film styles there are. Not for editing or converting existing video files."
```

新 description：

```json
"Direct and produce a short film made entirely in code, in one of the styles of the Lemo-Opuscar library (e.g. Impasto Oil Painting 油画厚涂, Watercolor Brush 水彩笔刷, Ukiyo-e 浮世绘, Satellite Briefing 卫星简报, Exploded Teardown 产品拆解, Microscope Story 显微叙事). Use when the user asks for a video, film, short, promo, explainer or animation (视频、短片、动画、宣传片) in a named style, including data, science and product explainers built from real material such as satellite imagery, laser scans, CAD files or archive scans (数据解说、科普、产品拆解); when they want a film made about their own topic and haven't chosen a style (help them choose); or when they ask which film styles there are. Not for editing or converting existing video files."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 74. markitdown-helper

- 入口文件：`/Users/zs/.agents/skills/markitdown-helper/SKILL.md`、`/Users/zs/.codex/skills/markitdown-helper/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/markitdown-helper/SKILL.md`

旧 description：

```json
"当用户需要把文件快速转成 Markdown（如 pdf/docx/pptx/xlsx/txt/csv/html/image/audio/url 等）时，优先调用 markitdown 自动生成可读文本。"
```

新 description：

```json
"将文件内容转成可读文本时用。不用于编辑原文件、保留版式或制作演示文稿。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": null
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": null
  }
}
```

## 75. media-use

- 入口文件：`/Users/zs/.agents/skills/media-use/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/media-use/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/media-use/agents/openai.yaml`

旧 description：

```json
"Get or make any media for a HyperFrames video - music, sound effects, images, icons, logos, voiceover, avatar and generated video, transcripts, cutouts, colour grades and looks - with HeyGen or free local tools, and mix placed audio. Also for footage that looks dark, flat or dull, or should be stylized or hidden."
```

新 description：

```json
"Get or make any media for a HyperFrames video - music, sound effects, images, icons, logos, voiceover, avatar and generated video, transcripts, cutouts, colour grades and looks - with HeyGen or free local tools, and mix placed audio. Also for footage that looks dark, flat or dull, or should be stylized or hidden."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 76. motion-graphics

- 入口文件：`/Users/zs/.agents/skills/motion-graphics/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/motion-graphics/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/motion-graphics/agents/openai.yaml`

旧 description：

```json
"A short, design-led motion graphic where motion is the message — kinetic typography, stat count-up, chart/data-viz hit, logo sting / brand lockup, lower-third / callout / social overlay, animated map (highlight regions, connect places, zoom to a location), animated tweet / news-article / headline, webpage / UI animation (scroll, cursor, callouts), or fusing a real image's geometry into a chart. Usually under 10s (up to ~30s), no narration or live-action subject; renders to MP4 or transparent overlay. Longer / narrated / multi-scene → /general-video. Unclear → /hyperframes.\n"
```

新 description：

```json
"A short, design-led motion graphic where motion is the message — kinetic typography, stat count-up, chart/data-viz hit, logo sting / brand lockup, lower-third / callout / social overlay, animated map (highlight regions, connect places, zoom to a location), animated tweet / news-article / headline, webpage / UI animation (scroll, cursor, callouts), or fusing a real image's geometry into a chart. Usually under 10s (up to ~30s), no narration or live-action subject; renders to MP4 or transparent overlay. Longer / narrated / multi-scene → /general-video. Unclear → /hyperframes.\n"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 77. music-to-video

- 入口文件：`/Users/zs/.agents/skills/music-to-video/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/music-to-video/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/music-to-video/agents/openai.yaml`

旧 description：

```json
"Turn a music track (an audio file, a video to pull audio from, or a track generated from a mood brief) into a beat-synced video — lyric video, slideshow, or kinetic promo. The music drives all pacing; any user-supplied images/videos are cut onto the same beat grid, and a complete video needs zero assets. Narrated pieces → the input-matched workflow (see /hyperframes). Unclear → /hyperframes."
```

新 description：

```json
"Turn a music track (an audio file, a video to pull audio from, or a track generated from a mood brief) into a beat-synced video — lyric video, slideshow, or kinetic promo. The music drives all pacing; any user-supplied images/videos are cut onto the same beat grid, and a complete video needs zero assets. Narrated pieces → the input-matched workflow (see /hyperframes). Unclear → /hyperframes."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 78. oa-issue-demand-closure

- 入口文件：`/Users/zs/.agents/skills/oa-issue-demand-closure/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/oa-issue-demand-closure/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/oa-issue-demand-closure/agents/openai.yaml`

旧 description：

```json
"当告警或测试已经确认是真实可修复问题时，使用 oa-mcp 创建 OA 问题任务和关联需求，完成 QID/DID 双向关联、幂等回读，并把编号交给分支开发流程。"
```

新 description：

```json
"当告警或测试已经确认是真实可修复问题时，使用 oa-mcp 创建 OA 问题任务和关联需求，完成 QID/DID 双向关联、幂等回读，并把编号交给分支开发流程。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 79. pr-to-video

- 入口文件：`/Users/zs/.agents/skills/pr-to-video/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/pr-to-video/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/pr-to-video/agents/openai.yaml`

旧 description：

```json
"Turn a GitHub pull request (a PR URL, owner/repo#N, or 'this PR' in a checked-out repo) into a code-change explainer video — changelog, feature reveal, fix, or refactor walkthrough built from the diff, commits, and files: the input is a code change, not a website. Not a product promo (/product-launch-video) or a no-PR topic explainer (/faceless-explainer). Unclear → /hyperframes."
```

新 description：

```json
"Turn a GitHub pull request (a PR URL, owner/repo#N, or 'this PR' in a checked-out repo) into a code-change explainer video — changelog, feature reveal, fix, or refactor walkthrough built from the diff, commits, and files: the input is a code change, not a website. Not a product promo (/product-launch-video) or a no-PR topic explainer (/faceless-explainer). Unclear → /hyperframes."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 80. product-launch-video

- 入口文件：`/Users/zs/.agents/skills/product-launch-video/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/product-launch-video/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/product-launch-video/agents/openai.yaml`

旧 description：

```json
"Turn a product or marketing URL, pasted script, or brief into a product launch / promo video — SaaS promos, feature reveals, product demos, app and company launches. Use when the user wants to market, launch, promote, or reveal a product; the default for any commercial URL. Site tours / showcases of a website route here too — the brief carries the show-it-as-is intent. Unclear → /hyperframes."
```

新 description：

```json
"Turn a product or marketing URL, pasted script, or brief into a product launch / promo video — SaaS promos, feature reveals, product demos, app and company launches. Use when the user wants to market, launch, promote, or reveal a product; the default for any commercial URL. Site tours / showcases of a website route here too — the brief carries the show-it-as-is intent. Unclear → /hyperframes."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 81. qa

- 入口文件：`/Users/zs/.agents/skills/qa/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/qa/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/qa/agents/openai.yaml`

旧 description：

```json
"Interactive QA session where user reports bugs or issues conversationally, and the agent files GitHub issues. Explores the codebase in the background for context and domain language. Use when user wants to report bugs, do QA, file issues conversationally, or mentions \"QA session\"."
```

新 description：

```json
"Interactive QA session where user reports bugs or issues conversationally, and the agent files GitHub issues. Explores the codebase in the background for context and domain language. Use when user wants to report bugs, do QA, file issues conversationally, or mentions \"QA session\"."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 82. qa-verification

- 入口文件：`/Users/zs/.agents/skills/qa-verification/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/qa-verification/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/qa-verification/agents/openai.yaml`

旧 description：

```json
"在修复分支合并或部署到 QA 后，验证原始告警是否消失、是否出现新问题，并决定是否允许建立正式 main 的 PR；QA 验收、发布后回归和部署验证时使用。"
```

新 description：

```json
"在修复分支合并或部署到 QA 后，验证原始告警是否消失、是否出现新问题，并决定是否允许建立正式 main 的 PR；QA 验收、发布后回归和部署验证时使用。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 83. skill-publisher

- 入口文件：`/Users/zs/.agents/skills/qiaomu-skill-publisher/SKILL.md`、`/Users/zs/.codex/skills/qiaomu-skill-publisher/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/qiaomu-skill-publisher/SKILL.md`

旧 description：

```json
"一键发布 agent skill 到 GitHub，自动验证 SKILL.md、生成或检查更吸引人的 README、区分 skill name 与 GitHub repo name、创建或更新仓库、推送并通过 npx skills 真实安装验证。当用户说\"发布这个skill\"、\"publish skill\"、\"把skill发到GitHub\"、\"分享这个skill\"、\"/publish-skill\"时触发。支持发布当前目录或指定路径的 skill。\n"
```

新 description：

```json
"发布技能到 GitHub 时用。不用于仅编写技能、本地安装或业务内容发布。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": null
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": null
  }
}
```

## 84. remotion-to-hyperframes

- 入口文件：`/Users/zs/.agents/skills/remotion-to-hyperframes/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/remotion-to-hyperframes/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/remotion-to-hyperframes/agents/openai.yaml`

旧 description：

```json
"Bring existing video code or footage into HyperFrames and verify it frame by frame against the original - Remotion first, also Motion Canvas, Lottie, Three.js, p5.js, canvas or plain HTML/CSS animation, or renders from Manim, After Effects or Blender. Use to port, convert, migrate or reuse work made with another tool."
```

新 description：

```json
"Bring existing video code or footage into HyperFrames and verify it frame by frame against the original - Remotion first, also Motion Canvas, Lottie, Three.js, p5.js, canvas or plain HTML/CSS animation, or renders from Manim, After Effects or Blender. Use to port, convert, migrate or reuse work made with another tool."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 85. repository-deployment-overview

- 入口文件：`/Users/zs/.agents/skills/repository-deployment-overview/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/repository-deployment-overview/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/repository-deployment-overview/agents/openai.yaml`

旧 description：

```json
"在告警确认并取得 OA QID/DID 后，定位真实仓库、最新 main、分支命名、测试命令和 QA/生产部署规则；跨仓库开发、发布、分支命名或部署依赖时使用。"
```

新 description：

```json
"在告警确认并取得 OA QID/DID 后，定位真实仓库、最新 main、分支命名、测试命令和 QA/生产部署规则；跨仓库开发、发布、分支命名或部署依赖时使用。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 86. review

- 入口文件：`/Users/zs/.agents/skills/review/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/review/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/review/agents/openai.yaml`

旧 description：

```json
"Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/PRD asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to \"review since X\"."
```

新 description：

```json
"Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/PRD asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to \"review since X\"."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 87. show-me

- 入口文件：`/Users/zs/.agents/skills/show-me/SKILL.md`、`/Users/zs/.codex/skills/show-me/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/show-me/SKILL.md`

旧 description：

```json
"Help the user understand the current topic visually with concise diagrams, code-shape sketches, and focused HTML artifacts."
```

新 description：

```json
"用图示解释当前问题时用。不用于正式海报、视频或完整产品界面制作。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": null
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": null
  }
}
```

## 88. slideshow

- 入口文件：`/Users/zs/.agents/skills/slideshow/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/slideshow/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/slideshow/agents/openai.yaml`

旧 description：

```json
"Build a HyperFrames slideshow to present live - slides, fragment reveals, branching hotspots and presenter mode with speaker notes, served by `hyperframes present` - or turn an existing page into one. Use when the person wants a deck or presentation rather than a rendered video."
```

新 description：

```json
"Build a HyperFrames slideshow to present live - slides, fragment reveals, branching hotspots and presenter mode with speaker notes, served by `hyperframes present` - or turn an existing page into one. Use when the person wants a deck or presentation rather than a rendered video."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 89. talking-head-recut

- 入口文件：`/Users/zs/.agents/skills/talking-head-recut/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/talking-head-recut/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/talking-head-recut/agents/openai.yaml`

旧 description：

```json
"Package an existing talking-head / interview / podcast video with timed, designed GRAPHIC OVERLAY cards — kinetic titles, lower-thirds, data callouts, quotes, side panels, picture-in-picture — synced to the transcript, on a 16:9 / 9:16 / 4:5 canvas of your choice; the clip plays untouched underneath. Trigger on \"graphic overlays\", \"on-screen graphics\", \"package / dress up my video\". Not plain subtitles (/embedded-captions). Unclear → /hyperframes."
```

新 description：

```json
"Package an existing talking-head / interview / podcast video with timed, designed GRAPHIC OVERLAY cards — kinetic titles, lower-thirds, data callouts, quotes, side panels, picture-in-picture — synced to the transcript, on a 16:9 / 9:16 / 4:5 canvas of your choice; the clip plays untouched underneath. Trigger on \"graphic overlays\", \"on-screen graphics\", \"package / dress up my video\". Not plain subtitles (/embedded-captions). Unclear → /hyperframes."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 90. tdd

- 入口文件：`/Users/zs/.agents/skills/tdd/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/tdd/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/tdd/agents/openai.yaml`

旧 description：

```json
"Test-driven development with red-green-refactor loop. Use when user wants to build features or fix bugs using TDD, mentions \"red-green-refactor\", wants integration tests, or asks for test-first development."
```

新 description：

```json
"Test-driven development with red-green-refactor loop. Use when user wants to build features or fix bugs using TDD, mentions \"red-green-refactor\", wants integration tests, or asks for test-first development."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 91. webapp-testing

- 入口文件：`/Users/zs/.agents/skills/webapp-testing/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/webapp-testing/SKILL.md`
- Codex 策略文件：`/Users/zs/.agents/skills/webapp-testing/agents/openai.yaml`

旧 description：

```json
"Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs."
```

新 description：

```json
"Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 92. xlsx

- 入口文件：`/Users/zs/.agents/skills/xlsx/SKILL.md`
- 实际修改文件：`/Users/zs/.agents/skills/xlsx/SKILL.md`

旧 description：

```json
"Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved."
```

新 description：

```json
"创建、编辑或分析电子表格时用。不用于纯文本说明、文档排版或演示文稿。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": null
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": null
  }
}
```

## 93. agent-reach

- 入口文件：`/Users/zs/.codex/skills/agent-reach/SKILL.md`
- 实际修改文件：`/Users/zs/.codex/skills/agent-reach/SKILL.md`

旧 description：

```json
"MUST USE when user wants to 调研/research/搜索/search/查/找/look up anything on the internet — e.g. 全网调研 X / 帮我调研一下 X / 查一下 X / 搜搜 X / 看看大家怎么评价 X / X 上有什么讨论 / research this topic。\nAlso MUST USE when user mentions any platform or shares any URL/链接: 小红书/xiaohongshu/xhs, Twitter/推特/X, B站/bilibili, Reddit, Facebook, Instagram, V2EX, LinkedIn/领英/Boss直聘/招聘/求职/jobs, YouTube, GitHub code search, 小宇宙播客, 雪球/股票行情, RSS feeds, or any web URL.\n16 platforms, multi-backend routing (OpenCLI / per-platform CLIs / APIs). Zero config for 6 channels. Run `agent-reach doctor --json` to see which backend serves each platform right now.\nNOT for: 写报告/数据分析/翻译等内容加工（本 skill 只负责从互联网获取内容）； 发帖/评论/点赞等写操作；已有专门 skill 的平台（先用专门 skill）。\n【路由方式】SKILL.md 包含路由表和常用命令，复杂场景需按需阅读对应分类的 references/*.md。 分类：search / social (小红书/推特/B站/V2EX/Reddit/Facebook/Instagram) / career(LinkedIn/Boss直聘) / dev(github) / web(网页/文章/RSS) / video(YouTube/B站/播客) / finance(雪球/股票)。\n"
```

新 description：

```json
"检索互联网或跨平台资料时用。不用于资料改写、发布互动或已有专用入口的平台操作。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": null
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": null
  }
}
```

## 94. bigpeng-hot-gzh

- 入口文件：`/Users/zs/.codex/skills/bigpeng-hot-gzh/SKILL.md`
- 实际修改文件：`/Users/zs/.local/skills/bigpeng-hot-gzh/SKILL.md`
- Codex 策略文件：`/Users/zs/.local/skills/bigpeng-hot-gzh/agents/openai.yaml`

旧 description：

```json
"为微信公众号生成爆款选题方向和候选标题。有明确选题、文章描述、草稿或草稿标题时，输出多条不同公式的候选标题；只有关键词、简单想法或未给输入时，先给选题方向再配标题。 用于用户提到爆款标题、公众号标题、起标题、选题、不知道写什么、候选标题、公众号选题、爆款公众号时。 只做选题和标题，不写正文。"
```

新 description：

```json
"为微信公众号生成爆款选题方向和候选标题。有明确选题、文章描述、草稿或草稿标题时，输出多条不同公式的候选标题；只有关键词、简单想法或未给输入时，先给选题方向再配标题。 用于用户提到爆款标题、公众号标题、起标题、选题、不知道写什么、候选标题、公众号选题、爆款公众号时。 只做选题和标题，不写正文。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 95. code-review

- 入口文件：`/Users/zs/.codex/skills/code-review/SKILL.md`
- 实际修改文件：`/Users/zs/.local/skills/mattpocock-skills/skills/engineering/code-review/SKILL.md`
- Codex 策略文件：`/Users/zs/.local/skills/mattpocock-skills/skills/engineering/code-review/agents/openai.yaml`

旧 description：

```json
"Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to \"review since X\"."
```

新 description：

```json
"Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to \"review since X\"."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 96. codebase-design

- 入口文件：`/Users/zs/.codex/skills/codebase-design/SKILL.md`
- 实际修改文件：`/Users/zs/.local/skills/mattpocock-skills/skills/engineering/codebase-design/SKILL.md`
- Codex 策略文件：`/Users/zs/.local/skills/mattpocock-skills/skills/engineering/codebase-design/agents/openai.yaml`

旧 description：

```json
"Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary."
```

新 description：

```json
"Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 97. codex-read-aloud

- 入口文件：`/Users/zs/.codex/skills/codex-read-aloud/SKILL.md`
- 实际修改文件：`/Users/zs/.codex/skills/codex-read-aloud/SKILL.md`

旧 description：

```json
"Manage the local Codex Read Aloud plugin that speaks Codex assistant responses on macOS. Use when the user asks to install, configure, test, disable, uninstall, debug, or explain Codex text-to-speech/read-aloud behavior."
```

新 description：

```json
"管理助手回答的语音朗读时用。不用于配音创作、录音转写或视频音轨制作。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": null
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": null
  }
}
```

## 98. diagnosing-bugs

- 入口文件：`/Users/zs/.codex/skills/diagnosing-bugs/SKILL.md`
- 实际修改文件：`/Users/zs/.local/skills/mattpocock-skills/skills/engineering/diagnosing-bugs/SKILL.md`
- Codex 策略文件：`/Users/zs/.local/skills/mattpocock-skills/skills/engineering/diagnosing-bugs/agents/openai.yaml`

旧 description：

```json
"Diagnosis loop for hard bugs and performance regressions. Use when the user says \"diagnose\"/\"debug this\", or reports something broken/throwing/failing/slow."
```

新 description：

```json
"Diagnosis loop for hard bugs and performance regressions. Use when the user says \"diagnose\"/\"debug this\", or reports something broken/throwing/failing/slow."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 99. domain-modeling

- 入口文件：`/Users/zs/.codex/skills/domain-modeling/SKILL.md`
- 实际修改文件：`/Users/zs/.local/skills/mattpocock-skills/skills/engineering/domain-modeling/SKILL.md`
- Codex 策略文件：`/Users/zs/.local/skills/mattpocock-skills/skills/engineering/domain-modeling/agents/openai.yaml`

旧 description：

```json
"Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or recording or editing an ADR."
```

新 description：

```json
"Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or recording or editing an ADR."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 100. dsh-find-simplifications

- 入口文件：`/Users/zs/.codex/skills/dsh-find-simplifications/SKILL.md`
- 实际修改文件：`/Users/zs/.local/skills/dsh-find-simplifications/SKILL.md`
- Codex 策略文件：`/Users/zs/.local/skills/dsh-find-simplifications/agents/openai.yaml`

旧 description：

```json
"Use when working in any codebase to find non-obvious simplification candidates, write proposed decision notes or inline TODO/FIXME/XXX notes, audit or coalesce superseded decision notes, or fold worthwhile simplification ideas from another PR; especially for dead, duplicated, speculative, over-built, added-then-removed, or hand-rolled-where-a-dependency-exists surfaces."
```

新 description：

```json
"Use when working in any codebase to find non-obvious simplification candidates, write proposed decision notes or inline TODO/FIXME/XXX notes, audit or coalesce superseded decision notes, or fold worthwhile simplification ideas from another PR; especially for dead, duplicated, speculative, over-built, added-then-removed, or hand-rolled-where-a-dependency-exists surfaces."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 101. dsh-merging-stacked-prs

- 入口文件：`/Users/zs/.codex/skills/dsh-merging-stacked-prs/SKILL.md`
- 实际修改文件：`/Users/zs/.local/skills/dsh-merging-stacked-prs/SKILL.md`
- Codex 策略文件：`/Users/zs/.local/skills/dsh-merging-stacked-prs/agents/openai.yaml`

旧 description：

```json
"Use when landing a stack of dependent GitHub PRs (A ← B ← C, where each bases on the one below) onto the default branch, merging a PR whose base is another open PR's branch, or whenever a request mentions \"stacked PRs\", \"PR stack\", \"dependent PRs\", or merging several related PRs in sequence. Requires every same-repository dependency chain to use GitHub's official stacked-PR feature before landing so GitHub owns stack-wide rules, CI, ordering, retargeting, and merge state."
```

新 description：

```json
"Use when landing a stack of dependent GitHub PRs (A ← B ← C, where each bases on the one below) onto the default branch, merging a PR whose base is another open PR's branch, or whenever a request mentions \"stacked PRs\", \"PR stack\", \"dependent PRs\", or merging several related PRs in sequence. Requires every same-repository dependency chain to use GitHub's official stacked-PR feature before landing so GitHub owns stack-wide rules, CI, ordering, retargeting, and merge state."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 102. dsh-prose-standard

- 入口文件：`/Users/zs/.codex/skills/dsh-prose-standard/SKILL.md`
- 实际修改文件：`/Users/zs/.local/skills/dsh-prose-standard/SKILL.md`
- Codex 策略文件：`/Users/zs/.local/skills/dsh-prose-standard/agents/openai.yaml`

旧 description：

```json
"Use when writing, reviewing, restoring, trimming, or auditing prose in any codebase, including deciding where documentation or comments are required across Markdown, JSDoc, code and test comments, prompts, descriptions, diagnostics, and CLI or UI strings."
```

新 description：

```json
"Use when writing, reviewing, restoring, trimming, or auditing prose in any codebase, including deciding where documentation or comments are required across Markdown, JSDoc, code and test comments, prompts, descriptions, diagnostics, and CLI or UI strings."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 103. dsh-trim-cot-leakage

- 入口文件：`/Users/zs/.codex/skills/dsh-trim-cot-leakage/SKILL.md`
- 实际修改文件：`/Users/zs/.local/skills/dsh-trim-cot-leakage/SKILL.md`
- Codex 策略文件：`/Users/zs/.local/skills/dsh-trim-cot-leakage/agents/openai.yaml`

旧 description：

```json
"Use when auditing or fixing prose that reads like a leaked reasoning transcript — dead design-session citations such as (decision N), audit item codes, or §N of uncommitted drafts; change narration such as \"used to\", \"no longer\", \"this cut\"; stack or review vantage (\"a later PR in this stack\", \"rejected in review\"); reviewer-addressed justifications; control-flow narration; or hedged planning residue in comments, JSDoc, docs, or decision notes."
```

新 description：

```json
"Use when auditing or fixing prose that reads like a leaked reasoning transcript — dead design-session citations such as (decision N), audit item codes, or §N of uncommitted drafts; change narration such as \"used to\", \"no longer\", \"this cut\"; stack or review vantage (\"a later PR in this stack\", \"rejected in review\"); reviewer-addressed justifications; control-flow narration; or hedged planning residue in comments, JSDoc, docs, or decision notes."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 104. goalfy-autodev

- 入口文件：`/Users/zs/.codex/skills/goalfy-autodev/SKILL.md`
- 实际修改文件：`/Users/zs/.codex/skills/goalfy-autodev/SKILL.md`

旧 description：

```json
"任意项目的轻量常驻开发入口，无需用户点名即可在需求分析、想法方案、架构设计、编码、缺陷修复、重构、性能优化、测试、开发者真人 Review、代码审查、PR/MR 评审、release/PRE 交付、发布和技术文档场景自动启用。普通任务直接在当前会话推进，复杂长任务按需建包；Goalfy 能力按项目叠加；Autofix 原 MR 指向 main，真人通过后集成当天已创建的下午 release 总分支并验证 CN-PRE，通过后自动合并原 MR、进入待发版。旧 goalfymax-autofix 显式调用兼容。"
```

新 description：

```json
"在 GoalfyAI 仓库开发或修缺陷时用。其他仓库用 project-aware-coding。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": null
  },
  "policy.allow_implicit_invocation": {
    "before": true,
    "after": true
  }
}
```

## 105. goalfymax-autofix

- 入口文件：`/Users/zs/.codex/skills/goalfymax-autofix/SKILL.md`
- 实际修改文件：`/Users/zs/.codex/skills/goalfymax-autofix/SKILL.md`
- Codex 策略文件：`/Users/zs/.codex/skills/goalfymax-autofix/agents/openai.yaml`

旧 description：

```json
"兼容旧的显式 goalfymax-autofix 调用；统一进入 Goalfy AutoDev，保留原 Autofix 缺陷命令、候选及运行状态。"
```

新 description：

```json
"兼容旧的显式 goalfymax-autofix 调用；统一进入 Goalfy AutoDev，保留原 Autofix 缺陷命令、候选及运行状态。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 106. grilling

- 入口文件：`/Users/zs/.codex/skills/grilling/SKILL.md`
- 实际修改文件：`/Users/zs/.local/skills/mattpocock-skills/skills/productivity/grilling/SKILL.md`
- Codex 策略文件：`/Users/zs/.local/skills/mattpocock-skills/skills/productivity/grilling/agents/openai.yaml`

旧 description：

```json
"Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases."
```

新 description：

```json
"Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 107. internal-comms

- 入口文件：`/Users/zs/.codex/skills/internal-comms/SKILL.md`
- 实际修改文件：`/Users/zs/.codex/skills/internal-comms/SKILL.md`
- Codex 策略文件：`/Users/zs/.codex/skills/internal-comms/agents/openai.yaml`

旧 description：

```json
"A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill whenever asked to write some sort of internal communications (status reports, leadership updates, 3P updates, company newsletters, FAQs, incident reports, project updates, etc.)."
```

新 description：

```json
"A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill whenever asked to write some sort of internal communications (status reports, leadership updates, 3P updates, company newsletters, FAQs, incident reports, project updates, etc.)."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 108. prototype

- 入口文件：`/Users/zs/.codex/skills/prototype/SKILL.md`
- 实际修改文件：`/Users/zs/.local/skills/mattpocock-skills/skills/engineering/prototype/SKILL.md`
- Codex 策略文件：`/Users/zs/.local/skills/mattpocock-skills/skills/engineering/prototype/agents/openai.yaml`

旧 description：

```json
"Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like."
```

新 description：

```json
"Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 109. record-browser-gif

- 入口文件：`/Users/zs/.codex/skills/record-browser-gif/SKILL.md`
- 实际修改文件：`/Users/zs/.local/skills/record-browser-gif/SKILL.md`
- Codex 策略文件：`/Users/zs/.local/skills/record-browser-gif/agents/openai.yaml`

旧 description：

```json
"Record browser or Web UI interaction demos as optimized GIFs using the available built-in browser, state-based frame capture, and deterministic encoding, then publish to a dedicated assets branch when the task includes attaching the GIF to a pull request. Use when asked to make, record, or generate a GIF that demonstrates a browser workflow, and for every pull request that changes product-user-visible GUI behavior, which MUST include a GIF recorded from the pull request's real server and model flow."
```

新 description：

```json
"Record browser or Web UI interaction demos as optimized GIFs using the available built-in browser, state-based frame capture, and deterministic encoding, then publish to a dedicated assets branch when the task includes attaching the GIF to a pull request. Use when asked to make, record, or generate a GIF that demonstrates a browser workflow, and for every pull request that changes product-user-visible GUI behavior, which MUST include a GIF recorded from the pull request's real server and model flow."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 110. research

- 入口文件：`/Users/zs/.codex/skills/research/SKILL.md`
- 实际修改文件：`/Users/zs/.local/skills/mattpocock-skills/skills/engineering/research/SKILL.md`
- Codex 策略文件：`/Users/zs/.local/skills/mattpocock-skills/skills/engineering/research/agents/openai.yaml`

旧 description：

```json
"Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent."
```

新 description：

```json
"Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 111. skill-eval

- 入口文件：`/Users/zs/.codex/skills/skill-eval/SKILL.md`
- 实际修改文件：`/Users/zs/.codex/skills/skill-eval/SKILL.md`

旧 description：

```json
"评测 business-app-creator Skill 的一个分支：开发者改完 Skill 说「测试一下 skills」「评测一下这个分支」「跑一下目标评测」「看看评测结果」时使用。用本机 skill-eval 工具，以开发者自己的 Codex 和 Goalfy QA 密钥，在 QA 从零做应用，分支版与对照版对跑，按测试目标给出能不能合的结论，并上传 OA「自动化skills评测看板」。只问 Skill 写法、不需要跑评测时不要用。"
```

新 description：

```json
"评测 business-app-creator 分支时用。不用于仅讨论 Skill 写法或无需运行评测的请求。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": null
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": null
  }
}
```

## 112. tdd

- 入口文件：`/Users/zs/.codex/skills/tdd/SKILL.md`
- 实际修改文件：`/Users/zs/.local/skills/mattpocock-skills/skills/engineering/tdd/SKILL.md`
- Codex 策略文件：`/Users/zs/.local/skills/mattpocock-skills/skills/engineering/tdd/agents/openai.yaml`

旧 description：

```json
"Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions \"red-green-refactor\", or wants integration tests."
```

新 description：

```json
"Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions \"red-green-refactor\", or wants integration tests."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 113. wechat-cli

- 入口文件：`/Users/zs/.codex/skills/wechat-cli/SKILL.md`
- 实际修改文件：`/Users/zs/.codex/skills/wechat-cli/SKILL.md`
- Codex 策略文件：`/Users/zs/.codex/skills/wechat-cli/agents/openai.yaml`

旧 description：

```json
"Read-only access to local WeChat chats through rion-wechat-cli, plus a guided first-access workflow when the user asks to connect their own account or obtain its local database keys. Use for chat search, contact history and unsent reply drafts; acquisition requires separate confirmation."
```

新 description：

```json
"Read-only access to local WeChat chats through rion-wechat-cli, plus a guided first-access workflow when the user asks to connect their own account or obtain its local database keys. Use for chat search, contact history and unsent reply drafts; acquisition requires separate confirmation."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 114. wechat-intelligence-hub

- 入口文件：`/Users/zs/.codex/skills/wechat-intelligence-hub/SKILL.md`
- 实际修改文件：`/Users/zs/.codex/skills/wechat-intelligence-hub/SKILL.md`

旧 description：

```json
"WeChat Intelligence Hub（微信个人情报库），本地只读微信情报 Skill。用于按任意明确时间范围，或围绕某条信息、某个人、某个群、某个产品/物品、某个微信标签、某个项目或事件检索和总结微信聊天；也用于生成群聊与私聊报告、发现并跟进商单/培训/咨询/项目合作、聚合跨群链接、检查待回复和待兑现承诺、维护商机状态及筛选值得复联的人。Use whenever the user invokes 微信个人情报库、WeChat Intelligence Hub、微信商单雷达、Deal Radar，或询问某人/某主题/某件事聊过什么、最近微信有什么新机会、谁需要回复或复联。"
```

新 description：

```json
"检索微信聊天或整理跟进事项时用。不用于发送消息、公众号发布或其他平台聊天。"
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": null
  },
  "policy.allow_implicit_invocation": {
    "before": true,
    "after": true
  }
}
```

## 115. wizard

- 入口文件：`/Users/zs/.codex/skills/wizard/SKILL.md`
- 实际修改文件：`/Users/zs/.local/skills/mattpocock-skills/skills/engineering/wizard/SKILL.md`
- Codex 策略文件：`/Users/zs/.local/skills/mattpocock-skills/skills/engineering/wizard/agents/openai.yaml`

旧 description：

```json
"Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. Don't invoke this for steps the agent can perform itself."
```

新 description：

```json
"Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. Don't invoke this for steps the agent can perform itself."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 116. writing-for-agents

- 入口文件：`/Users/zs/.codex/skills/writing-for-agents/SKILL.md`
- 实际修改文件：`/Users/zs/.local/skills/mattpocock-skills/skills/productivity/writing-for-agents/SKILL.md`
- Codex 策略文件：`/Users/zs/.local/skills/mattpocock-skills/skills/productivity/writing-for-agents/agents/openai.yaml`

旧 description：

```json
"Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md."
```

新 description：

```json
"Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 117. xilo-opus-video

- 入口文件：`/Users/zs/.codex/skills/xilo-opus-video/SKILL.md`
- 实际修改文件：`/Users/zs/.codex/skills/xilo-opus-video/SKILL.md`
- Codex 策略文件：`/Users/zs/.codex/skills/xilo-opus-video/agents/openai.yaml`

旧 description：

```json
"Make videos with code (Canvas / HTML-CSS-SVG / WebGL shaders / Three.js / Remotion / HyperFrames / Manim + code-synthesized sound), rendered frame by frame with Playwright + FFmpeg. Asks what the user wants to make (an idea, source content such as an article, script, product page or codebase, or a reference video), proposes three distinct video plans with shot-by-shot visual summaries, renders a key-frame still or a few-second preview for each, and after the user confirms one, writes the full brief and builds the finished MP4. Use whenever someone wants Claude to make, animate or render a video, motion graphic, animated explainer, product promo, kinetic-typography piece, pixel-art or retro animation, UI motion demo, or wants to recreate the look of a reference video in code — including Chinese requests like「做个视频」「用代码做视频」「做个动效」「做个宣传片」「帮我复刻这个视频」 「Opus 做视频」. Also use when the user has AI-generated character clips (green screen) and wants code-built scenes around them. Not for generating footage with video models, editing in Premiere/CapCut/AE, or subtitling an existing video."
```

新 description：

```json
"Make videos with code (Canvas / HTML-CSS-SVG / WebGL shaders / Three.js / Remotion / HyperFrames / Manim + code-synthesized sound), rendered frame by frame with Playwright + FFmpeg. Asks what the user wants to make (an idea, source content such as an article, script, product page or codebase, or a reference video), proposes three distinct video plans with shot-by-shot visual summaries, renders a key-frame still or a few-second preview for each, and after the user confirms one, writes the full brief and builds the finished MP4. Use whenever someone wants Claude to make, animate or render a video, motion graphic, animated explainer, product promo, kinetic-typography piece, pixel-art or retro animation, UI motion demo, or wants to recreate the look of a reference video in code — including Chinese requests like「做个视频」「用代码做视频」「做个动效」「做个宣传片」「帮我复刻这个视频」 「Opus 做视频」. Also use when the user has AI-generated character clips (green screen) and wants code-built scenes around them. Not for generating footage with video models, editing in Premiere/CapCut/AE, or subtitling an existing video."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": null,
    "after": false
  }
}
```

## 118. yingzao

- 入口文件：`/Users/zs/.codex/skills/yingzao/SKILL.md`
- 实际修改文件：`/Users/zs/.codex/skills/yingzao/SKILL.md`
- Codex 策略文件：`/Users/zs/.codex/skills/yingzao/agents/openai.yaml`

旧 description：

```json
"Transform real Chinese architecture and place-based cultural photos into art-directed editorial posters, integrated multi-photo scenes, and optional source comparisons. Use for historic buildings, vernacular streets, culturally rooted shops, interiors, food, travel covers, and place montages; do not use for generic advertising, routine retouching, or invented places."
```

新 description：

```json
"Transform real Chinese architecture and place-based cultural photos into art-directed editorial posters, integrated multi-photo scenes, and optional source comparisons. Use for historic buildings, vernacular streets, culturally rooted shops, interiors, food, travel covers, and place montages; do not use for generic advertising, routine retouching, or invented places."
```

调用策略：

```json
{
  "disable-model-invocation": {
    "before": null,
    "after": true
  },
  "policy.allow_implicit_invocation": {
    "before": true,
    "after": false
  }
}
```
