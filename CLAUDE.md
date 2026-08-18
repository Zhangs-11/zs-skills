# zs-skills 使用说明

本仓库包含 Kakarot 维护的 Agent Skills。Claude Code、Codex 和其他兼容工具应从实际安装目录解析每项 Skill 的 `scripts/`、`references/`、`assets/` 和 `tools/`，不要假定它一定安装在某个固定的隐藏目录。

## 安装与发现

安装全部 Skills：

```bash
npx skills add Zhangs-11/zs-skills
```

只安装一项时使用 `--skill <name>`。安装后可通过下面的命令核对仓库中的可发现名称：

```bash
npx skills add Zhangs-11/zs-skills --list
```

## 全局双向钢人入口

每个新的任务型用户消息先使用 `steelman-before-answer`，在后台重述真正问题、钢人支持方和反对方并寻找关键变量，默认不展示过程。无需用户选择时直接回答或执行；只有存在无法自查、会实质改变结果的用户选择时，才说明最短影响并问一个原子问题。用户回答后继续原任务，不重新审问；只有明确要求时才展开完整双向钢人。

这项 Skill 是交互入口，不代替领域 Skill。实质性判断继续使用 `first-principles-adversarial-review`；需求澄清、问题诊断、代码 Review 和实现分别交给对应 Skill。

## 默认推理与核验

需求、设计、诊断、评审、建议和修改等实质性任务，优先使用 `first-principles-adversarial-review` 作为底层推理与核验 Skill。它先区分真实目标、事实、约束和未经验证的假设，再追踪生产者、消费者、上下游与替代方案，并主动寻找能推翻初步结论的证据。

这项 Skill 可以与仓库内其他领域 Skill 叠加：例如 `peer-pr-review` 负责 CodeUp PR 的具体审查流程，`first-principles-adversarial-review` 负责避免顺着 PR 描述接受未经验证的根因。纯翻译、忠实转写、机械格式转换和无判断的一步操作不需要加载。

## 需求澄清与问题诊断

用户要求实现需求、修改功能、设计方案或完成复杂任务，且背景、范围、约束或验收标准仍有实质性歧义时，使用 `clarify-before-action`。先只读调查可自行确认的事实，再以苏格拉底方式一次只问一个关键问题；整理背景、需求、痛点、拟执行范围和明确不做事项，经用户确认后才能进入实现。事实清楚、低风险且可逆的一步操作无需强行追问。

用户要求分析报错、排查异常、寻找根因或解释“为什么会发生”时，使用 `diagnose-and-explain`。它覆盖技术、数据、业务、产品和流程问题：优先读取代码、日志、配置、数据和规则，建立安全的反馈或证据闭环，通过多个可证伪假设寻找反证，并用小白能理解的语言、例子或必要图示解释。只在缺少关键事实时一次问一个问题。

两项 Skill 都使用 `first-principles-adversarial-review` 作为推理底盘。只读调查无需确认；修改代码、配置、测试、文档或数据，以及提交、推送、部署、发消息和其他外部写操作，必须先说明拟执行范围并获得明确确认。需求确认和诊断结论都不能自动扩张成删除或发布授权。

## 长文写作工作流

用户说“帮我写篇文章”“按我的风格写”或提供链接、PDF、brief、采访和笔记要求出稿时，使用 `kakarot-writer`。

`kakarot-writer` 是个人长文总调度：它先确定 Kakarot 的作者位置、真实材料、核心判断和文章原型，再调用 `human-writing` 生成正文，最后完成个人风格复核、标题、截图与来源、正文配图、`21:9` 主封面和 `1:1` 分享封面。

“帮我写篇文章”默认表示完整交付，不需要另问用户是否需要标题和封面。公众号长文是首发载体，也是知乎、博客、掘金、小红书、抖音和B站共同使用的唯一内容母稿。长文平台可以原样同步正文和标题；小红书、抖音和B站视频交给 `kakarot-repurposer` 调整长度、节奏与画面，但不能改变母稿中的事实、核心判断、作者态度和来源。

封面优先调用 `guizang-social-card-skill` 的 B 方案，使用官网、官方文档、公告、GitHub 等真实素材。只有专用 Skill 不可用时才回退到 AI 图片，并向用户说明。

写完整成品不代表获得发布授权。只有用户明确说“存到公众号”“发到草稿箱”或“发布”时，才调用 `wechat-publisher` 写入微信公众号。

## 微信公众号发布

发布前先确认文章、标题、摘要、正文图片和封面均已完成，并执行 `wechat-publisher` 的只读预检。凭证从 `~/.wechat-publisher/.env` 读取，不写进仓库，也不在日志和回复中回显。

首次使用时，在实际的 `wechat-publisher` Skill 目录内安装 CLI 依赖：

```bash
cd <wechat-publisher-skill-dir>/tools/wechat-publisher
python3 -m venv venv
venv/bin/pip install .
```

凭证文件示例：

```dotenv
WECHAT_APP_ID=wx你的AppID
WECHAT_APP_SECRET=你的AppSecret
WECHAT_AUTHOR=卡卡罗特
WECHAT_DEFAULT_COVER_MEDIA_ID=你的封面media_id
```

如果发布失败并返回 `40164`，只需告诉用户当前公网 IP 需要加入微信公众号后台白名单；其他错误应报告实际原因和下一步，不自动改凭证或外部配置。

## 代码 Review 协作

用户提供同事的需求背景和 CodeUp PR，要求判断根因、改动合理性或遗漏时，使用 `peer-pr-review`。它是只读审查：先固定真实 diff 和最新远端，再按需核对上下游、项目规范、运行时配置和日志；不自动修改代码或在 PR 上评论、通过、合并。

用户要把自己的 PR 整理成 Markdown 发给同事时，使用 `review-handoff`。文档顶部必须逐仓列出 PR，正文用背景、问题、根因、改前改后、验证和 Review 重点减少接手成本。它负责交接，不替 reviewer 给通过结论。

用户要在会议或上线前用一小段介绍改动时，使用 `change-meeting-brief`。默认只讲问题、改之前为什么出错和这次如何解决，控制在约 20～40 秒，不展开代码细节。

三项 Skill 都必须区分最新代码、实际部署和本次运行事实；无法验证的根因或环境行为不得写成确定结论。

## 维护约定

- 每个 Skill 的触发条件、工作流和边界以该目录的 `SKILL.md` 为准。
- 个人写作规则由 `kakarot-writer` 管理；通用材料、现实边界和自然中文机制由 `human-writing` 管理。
- 修改 Skill 后先做结构验证、本地发现和安装测试；未经用户明确授权，不 commit、push 或发布。
- 所有 `你的xxx` 都是占位符，真实凭证不得进入 Git。
