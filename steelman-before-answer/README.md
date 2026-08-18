# steelman-before-answer

> AI 应该在后台把正反双方想完整，而不是让你每次先读一份思考报告。

steelman-before-answer 会在回答前内部重述问题、钢人支持方和反对方、寻找真正分歧与关键变量。默认只把最终结论和必要证据展示给你；只有确实需要你决定的变量，才用最短背景说明影响并一次问一个问题。

<p align="center">
  <a href="https://github.com/Zhangs-11/zs-skills/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/Zhangs-11/zs-skills?style=flat-square&logo=github" /></a>
  <a href="https://github.com/Zhangs-11/zs-skills/commits/main"><img alt="Last commit" src="https://img.shields.io/github/last-commit/Zhangs-11/zs-skills?style=flat-square&logo=git" /></a>
  <a href="../LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" /></a>
</p>

## 实际效果

简单、明确的任务直接处理：

```text
用户：把“这个接口会在任务完成后发送通知”翻译成英文。
助手：This endpoint sends a notification when the task is complete.
```

只有真正需要用户决定时才暂停：

```text
用户：把用户偏好同步从轮询改成事件推送，直接给方案。
助手：轮询、纯推送和混合方案的主要差异在故障后的收敛方式。
      业务允许偏好在多长时间内最终一致？
```

遇到重要取舍时，Skill 会自动用三段白话展开，不需要用户记口令：

```text
我的判断：不建议把所有服务一刀切改成事件驱动；需要即时结果和强一致性的调用仍适合同步。

两个方向的差别：全面事件化能降低同步耦合，但会增加幂等、乱序、补偿和排障成本；选择性事件化只改造多消费者、可异步恢复的业务事实，收益更可控。

只需要你确认：你当前更想解决同步调用的故障扩散，还是新增消费者总要修改上游的问题？
```

## 安装

```bash
npx skills add Zhangs-11/zs-skills --skill steelman-before-answer
```

验证仓库中可以发现该 Skill：

```bash
npx skills add Zhangs-11/zs-skills --list
```

Codex 与 Claude Code 可以共用同一份 `.local` 源：

```bash
ln -s /path/to/zs-skills/steelman-before-answer ~/.codex/skills/steelman-before-answer
ln -s /path/to/zs-skills/steelman-before-answer ~/.claude/skills/steelman-before-answer
```

## 推荐的全局入口

在 Codex 的全局 `AGENTS.md` 和 Claude Code 的全局 `CLAUDE.md` 中加入：

```markdown
每个新任务先使用 `$steelman-before-answer` 在后台完成正反钢人和关键变量审查。无需用户选择时直接回答或执行；普通缺口只问一个原子问题；存在两个真正可行且代价明显不同的方向时，自动展示“我的判断 / 两个方向的差别 / 只需要你确认”三段白话，不依赖用户输入触发口令。
```

## 默认可见内容

| 情况 | 用户看到什么 |
|---|---|
| 可查事实、翻译、转写、格式转换 | 直接答案或成品 |
| 明确且可逆的执行任务 | 执行结果和必要验证 |
| 存在会改变行为的用户选择 | 最短影响说明 + 一个问题 |
| 用户回答上一轮问题 | 判断、理由和继续后的结果 |
| 两个可行方向且选错代价明显 | 自动三段白话版，控制在一屏内 |

后台审查不会消失，只是不再把内部过程变成阅读负担。

## 你可以这样说

- “这个方案靠谱不？”
- “帮我找一下真正根因。”
- “直接修改这个文件。”
- “这两个方案应该选哪个？”

## 前置条件

- [ ] 使用支持 Agent Skills 的 Codex、Claude Code 或其他兼容工具。
- [ ] 安装后新开会话，让工具重新发现 Skill。
- [ ] 若要稳定覆盖全部任务，在对应全局规则文件中加入上面的入口。
- [ ] 实质性判断建议同时安装 `first-principles-adversarial-review`；代码 Review 建议同时安装 `peer-pr-review`。

本 Skill 没有 Python、Node.js、账号或外部 API 依赖。

## 边界

- 后台钢人不等于泄露隐藏思维链；用户只看到结论、证据和必要确认。
- 能通过代码、配置、日志、数据库只读查询或权威来源确认的事实，不会反问用户。
- 用户对确认问题的回答不会自动扩大成删除、commit、push、部署或数据库写入授权。
- 领域 Skill 仍负责调查和执行；本 Skill 只负责避免顺着未经检查的前提直接回答。

## Troubleshooting

| 问题 | 原因 | 解决方法 |
|---|---|---|
| 每次仍展示完整正反论证 | 全局规则仍要求可见五段模板 | 改为后台审查，仅在重要取舍时自动展示三段白话 |
| 简单任务仍被追问 | 把可查事实或低价值偏好误判成用户选择 | 先查事实；不影响目标的细节采用项目惯例 |
| 一次问了多个问题 | 没有选择最上游变量 | 只保留最可能改变结果的一个原子问题 |
| 回答后又重新提问 | 没识别为上一轮确认答案 | 保留对话上下文，并继续原任务而非重启钢人 |

完整执行协议见 [SKILL.md](SKILL.md)。
