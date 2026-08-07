# first-principles-adversarial-review

> AI 最危险的不是不会回答，而是沿着错误前提给出一个听起来很完整的答案。

first-principles-adversarial-review 把“先从真实目标和机制重新推导，再主动寻找反证”变成 Agent 的默认工作方式。它不会把每个简单问题都写成长篇分析，但会在需求、设计、诊断、评审和修改任务中检查事实源、上下游、替代方案、失败路径与未验证假设。

<p align="center">
  <a href="https://github.com/Zhangs-11/zs-skills/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/Zhangs-11/zs-skills?style=flat-square&logo=github" /></a>
  <a href="https://github.com/Zhangs-11/zs-skills/commits/main"><img alt="Last commit" src="https://img.shields.io/github/last-commit/Zhangs-11/zs-skills?style=flat-square&logo=git" /></a>
  <a href="../LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" /></a>
</p>

## 它会改变什么

没有这项 Skill 时，Agent 容易顺着用户给出的方案或根因继续推演：

```text
“把轮询改成事件推送。”
→ 直接设计消息格式和消费者。
```

启用后，它会先拆开“目标”和“方案”，再攻击自己的初步结论：

```text
真实目标：降低同步延迟，还是降低服务压力？
事实源：当前由谁写入偏好，哪些消费者读取？
机制：推送丢失、重复、乱序时怎样恢复？
替代：保留低频对账的混合方案是否更稳？
结论：给出经过验证的最小方案，并标注仍未核实的项目事实。
```

它不是“凡事反对”，也不是要求从零重造系统。第一性原理负责找到真正的问题和不变量；对抗式审查负责确认准备采用的结论经得起反证。

## 安装

安装这一项 Skill：

```bash
npx skills add Zhangs-11/zs-skills --skill first-principles-adversarial-review
```

查看仓库中可发现的 Skill：

```bash
npx skills add Zhangs-11/zs-skills --list
```

安装后新开一次 Claude Code、Codex 或其他 Agent Skills 兼容工具的会话。

## 你可以这样说

- “产品说加二次确认框就能避免误删，分析一下这个需求。”
- “我觉得昨晚的超时就是 Redis 升级导致的，帮我判断根因。”
- “设计订单创建后的积分发放流程，要求绝不能重复发积分。”
- “Review 这个方案，重点找事实源、遗漏分支和反例。”

这项 Skill 的目标是自动介入实质性任务，因此通常不需要显式说“使用第一性原理”或“做对抗式审查”。如果所用 Agent 会保守地按需加载 Skill，可以在全局 `AGENTS.md` 或 `CLAUDE.md` 中加入：

```markdown
所有包含事实判断、原因分析、需求、设计、诊断、评审、建议或修改的实质性任务，必须先读取并使用完整的 `$first-principles-adversarial-review`。纯翻译、忠实转写、机械格式转换和无判断的一步操作不强制加载。
```

## 场景路由

| 场景 | 第一性原理 | 对抗式审查 |
|---|---|---|
| 需求、产品设计、技术方案、架构 | 使用 | 使用 |
| 故障诊断、性能和根因分析 | 使用 | 使用 |
| 代码、配置、流程或文档修改 | 使用 | 使用 |
| 事实查询、总结、数据解读 | 视口径是否有歧义 | 使用 |
| 纯翻译、忠实转写、机械格式转换 | 不使用 | 仅检查明显错误 |

审查深度会随错误代价变化：低风险任务只做轻量检查；影响方案、代码或多人协作时核对事实源、上下游和替代方案；生产、安全、隐私、法律、财务或不可逆操作需要更深入的独立证据。

## 前置条件

- [ ] 使用支持 Agent Skills 的工具；安装后用 `npx skills add Zhangs-11/zs-skills --list` 验证发现。
- [ ] 若希望几乎所有实质性任务都稳定加载，在全局 `AGENTS.md` 或 `CLAUDE.md` 中加入上面的强制路由规则。
- [ ] 涉及代码、日志、数据库或远端状态时，为 Agent 提供对应只读权限；没有证据时，Skill 只会给出明确标注的推断。

本 Skill 本身没有 Python、Node.js 或外部 API 依赖。

## 测试

仓库包含六类行为用例与可重复脚本：

```bash
./evals/run_codex_evals.sh
./evals/run_trigger_stability.sh
```

测试覆盖技术方案、故障归因、运营因果判断、删除需求、已确定技术约束和简单翻译负例。首次公开版本在本地 Codex 新会话中完成 23 条行为断言，全部通过；最易欠触发的正例重复 3 次全部加载，翻译负例重复 3 次全部跳过。

## 边界与限制

- Skill 能提高触发概率，但不同 Agent 对按需加载的实现不同；需要强确定性时，应配合全局规则显式路由。
- 对抗式审查依赖可访问的证据。没有项目代码、日志或配置时，不会把通用经验包装成已验证事实。
- 第一性原理不会推翻用户已经明确拍板的约束；它会在约束内寻找不变量、集成点和失败路径。
- 审查发现问题不等于获得修改、删除、提交、推送、部署或数据库写入授权。
- 纯翻译和机械操作默认不加载，避免不必要的上下文和阅读成本。

## Troubleshooting

| 问题 | 原因 | 解决方法 |
|---|---|---|
| 安装后没有自动触发 | Agent 认为任务可以直接处理，或当前会话没有刷新 Skill 清单 | 新开会话，并在全局规则中加入上面的强制路由句 |
| 每次回答都出现很长的检查表 | Agent 把内部方法误当成固定输出模板 | 明确要求“只展示结论、证据和关键不确定性，不展示完整内部检查过程” |
| 简单翻译也加载了 Skill | 全局路由没有排除机械任务 | 在路由规则中保留“纯翻译、转写、格式转换不强制加载” |
| 结论仍然只有通用经验 | 缺少可读取的事实源 | 提供项目目录、日志、配置、数据口径或权威链接，并允许只读核验 |

完整执行方法见 [SKILL.md](SKILL.md)。
