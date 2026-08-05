# zs-skills 使用说明

本仓库包含张硕维护的 Agent Skills。Claude Code、Codex 和其他兼容工具应从实际安装目录解析每项 Skill 的 `scripts/`、`references/`、`assets/` 和 `tools/`，不要假定它一定安装在某个固定的隐藏目录。

## 安装与发现

安装全部 Skills：

```bash
npx skills add Zhangs-11/zs-skills
```

只安装一项时使用 `--skill <name>`。安装后可通过下面的命令核对仓库中的可发现名称：

```bash
npx skills add Zhangs-11/zs-skills --list
```

## 长文写作工作流

用户说“帮我写篇文章”“按我的风格写”或提供链接、PDF、brief、采访和笔记要求出稿时，使用 `kakarot-writer`。

`kakarot-writer` 是个人长文总调度：它先确定张硕的作者位置、真实材料、核心判断和文章原型，再调用 `human-writing` 生成正文，最后完成个人风格复核、标题、截图与来源、正文配图、`21:9` 主封面和 `1:1` 分享封面。

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

## 维护约定

- 每个 Skill 的触发条件、工作流和边界以该目录的 `SKILL.md` 为准。
- 个人写作规则由 `kakarot-writer` 管理；通用材料、现实边界和自然中文机制由 `human-writing` 管理。
- 修改 Skill 后先做结构验证、本地发现和安装测试；未经用户明确授权，不 commit、push 或发布。
- 所有 `你的xxx` 都是占位符，真实凭证不得进入 Git。
