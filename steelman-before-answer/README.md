# steelman-before-answer

> 你问 AI 一个重要问题，它往往顺着你的表述立刻给答案；真正危险的是，问题本身可能还没想清楚。

steelman-before-answer 把回答拆成两个回合：先替支持方和反对方分别构造最强论证，找出真正分歧，只问一个最可能改变结论的问题；等你回答后，再给出明确判断、理由和下一步行动。

<p align="center">
  <a href="https://github.com/Zhangs-11/zs-skills/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/Zhangs-11/zs-skills?style=flat-square&logo=github" /></a>
  <a href="https://github.com/Zhangs-11/zs-skills/commits/main"><img alt="Last commit" src="https://img.shields.io/github/last-commit/Zhangs-11/zs-skills?style=flat-square&logo=git" /></a>
  <a href="../LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" /></a>
</p>

## 实际效果

第一回合不会抢答：

```text
真正的问题
你要决定的不是“要不要上消息队列”，而是怎样在不重复发积分的前提下可靠解耦订单与积分。

支持当前想法的最强论证
……

反对当前想法的最强论证
……

真正分歧与关键变量
关键不是队列本身，而是业务是否允许积分延迟到账，以及谁拥有最终幂等事实源。

最关键的问题
积分可以延迟到账吗？
```

你回答后，第二回合才给判断并继续原任务：

```text
明确判断
采用消息队列，但以订单号和积分规则版本建立业务唯一键，不依赖队列的“恰好一次”。

理由
……

下一步行动
……
```

## 安装

```bash
npx skills add Zhangs-11/zs-skills --skill steelman-before-answer
```

安装后用下面的命令确认能发现：

```bash
npx skills add Zhangs-11/zs-skills --list
```

如果希望 Codex 与 Claude Code 共用同一份本地源，可以把仓库放在 `.local`，再建立软链接：

```bash
ln -s /path/to/zs-skills/steelman-before-answer ~/.codex/skills/steelman-before-answer
ln -s /path/to/zs-skills/steelman-before-answer ~/.claude/skills/steelman-before-answer
```

## 让它成为默认入口

Skill 的描述会提高自动触发率；要保证每个新任务都先进入双向钢人，在 Codex 的全局 `AGENTS.md` 和 Claude Code 的全局 `CLAUDE.md` 中加入：

```markdown
每个新的任务型用户消息必须先读取并使用完整的 `$steelman-before-answer`。第一阶段完成双向钢人，只问一个最关键问题并停止；用户回答后进入第二阶段给出判断、理由和下一步，不得重新启动同一轮钢人。
```

## 你可以这样说

- “我准备把所有同步逻辑都改成事件驱动，你怎么看？”
- “这个故障肯定是 Redis 升级导致的，帮我排查。”
- “把这句话翻成英文。”
- “直接帮我实现删除按钮的二次确认。”

即使用户没有说“钢人论证”，它也会先把问题、正反双方和关键变量拼完整。事实题和机械任务不会虚构相反事实，而是比较不同口径、语境或执行方式。

## 两阶段协议

| 阶段 | 做什么 | 何时结束 |
|---|---|---|
| 第一阶段 | 重述真正问题、钢人支持方、钢人反对方、找出分歧与变量 | 恰好问一个关键问题后停止 |
| 第二阶段 | 吸收回答、给出判断和理由、继续原任务 | 下一步明确且不越过授权边界 |

如果最新消息是在回答上一轮问题，Skill 会进入第二阶段，而不是因为全局规则再次从头钢人。`好的`、`继续`、`按这个来` 等纯确认也不会被误判成新任务。

## 前置条件

- [ ] 使用支持 Agent Skills 的 Codex、Claude Code 或其他兼容工具。
- [ ] 安装后新开会话，让工具重新发现 Skill。
- [ ] 若要求稳定覆盖所有任务，在对应全局规则文件中加入上面的入口句。
- [ ] 实质性判断建议同时安装 `first-principles-adversarial-review`；代码 Review 建议同时安装 `peer-pr-review`。

本 Skill 没有 Python、Node.js、账号或外部 API 依赖。

## 边界

- 它会让每个新任务至少多一个交互回合，这是覆盖优先的主动取舍。
- 它展示的是可核验的论证结构，不要求模型泄露隐藏思维链。
- 双向钢人不等于机械五五开；证据明显不对称时会明确说明。
- 用户对关键问题的回答不会自动扩大成删除、commit、push、部署或数据库写入授权。
- 领域 Skill 仍负责真实调查和执行；本 Skill 只负责先探索、后判断的对话闸门。

## Troubleshooting

| 问题 | 原因 | 解决方法 |
|---|---|---|
| 新问题仍被直接回答 | 当前会话未刷新，或全局入口太弱 | 新开会话，并在 `AGENTS.md` / `CLAUDE.md` 加入强制入口句 |
| 回答关键问题后又从头钢人 | Agent 没识别当前处于第二阶段 | 保留完整对话上下文，并确认全局规则包含“不得重新启动同一轮” |
| 反方像为了反对而反对 | 任务没有天然立场却被制造了相反事实 | 要求比较口径、语境或执行方式，并指出证据不对称 |
| 一次问了多个问题 | 关键变量没有排序 | 要求只保留最可能改变结论的一个变量和一个独立问句 |

完整执行协议见 [SKILL.md](SKILL.md)。
