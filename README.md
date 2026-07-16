# zs-skills

Kakarot 的个人 Claude Code Skill 合集。

帮你写公众号文章、查 AI 资讯、画架构图，一条龙搞定。

---

## 技能一览

| Skill | 能做什么 | 怎么触发（对 Claude 说） |
|-------|---------|------------------------|
| **kakarot-writer** | 按「卡卡罗特学AI」的风格写公众号长文 | "帮我写篇文章"、"写稿子"、"按我的风格写" |
| **kakarot-repurposer** | 把公众号长文一稿改写成小红书笔记 + 抖音脚本（含 AI 配音、字幕、效果预览页） | "转成小红书"、"改成抖音脚本"、"一稿多平台" |
| **fable-writer** | 用精炼的寓言解释抽象概念，附概念解析和检验问题 | "写寓言解释XX"、"用寓言讲明白"、"fable" |
| **wechat-publisher** | 把写好的文章一键存到微信草稿箱 | "存到公众号"、"发到草稿箱"、"推到公众号" |
| **aihot** | 查 AI 圈今天发生了什么 | "AI 圈"、"AI 日报"、"今天 AI 有什么新闻" |
| **ai-hot-picker** | 从 AI HOT 日报中挑选公众号选题，智能推荐 + 一键写推文或长文 | "选题"、"今天写什么"、"写推文"、"有什么热点" |
| **system-structure-diagram** | 按参考图风格生成系统结构图 | "画系统架构图"、"按这个样式画图" |
| **life-designer** | 斯坦福人生设计课方法论，多轮对话生成三个五年奥德赛计划，产出《个人人生设计蓝图》 | "帮我设计人生"、"人生规划"、"我很迷茫" |
| **resume-optimizer** | 以技术面试官视角写简历、改简历、评审简历 | "帮我优化简历"、"写一份简历"、"评审下我的简历" |
| **dating-chat-coach** | 异性线上聊天全流程指南（相亲/网上认识两套打法）：接话、转微信、约见面、安全防线 | "她说XX怎么回"、"相亲怎么开场"、"该约见面吗" |

> 两个配合使用效果最好：`kakarot-writer` 写文章 → `wechat-publisher` 存到公众号，一条龙。

---

## 前置条件

每个 skill 需要的东西都在这里，**没有额外依赖的就不需要装任何东西**。

| Skill | 需要准备 |
|-------|---------|
| **kakarot-writer** | 什么都不用装。安装后直接对 Claude 说"帮我写篇文章"就行。 |
| **fable-writer** | 什么都不用装。安装后直接说"写寓言解释XX"就行。 |
| **aihot** | 什么都不用装。安装后直接问"AI 圈有什么"就行。底层调公开 API，不需要 API Key。 |
| **ai-hot-picker** | 什么都不用装。安装后说"选题"或"写推文"就行。底层调 AI HOT 公开 API。 |
| **life-designer** | 什么都不用装。安装后直接说"帮我设计人生"就行。 |
| **resume-optimizer** | 什么都不用装。安装后直接说"帮我优化简历"就行。 |
| **dating-chat-coach** | 什么都不用装。安装后直接问"她说XX我怎么回"就行。 |
| **system-structure-diagram** | 需要装好 [Inkscape](https://inkscape.org/release/)（SVG 转 PNG 用）。macOS: `brew install inkscape`。Windows/Linux 去官网下载。 |
| **wechat-publisher** | 需要准备两样东西：<br>1. **Python 3.12+**（macOS: `brew install python@3.13`）<br>2. **公众号 AppID 和 AppSecret**（去 mp.weixin.qq.com → 开发 → 基本配置 获取）<br>3. **公网 IP 加入白名单**（装好后运行时报错会告诉你当前 IP，去后台加一下就行） |

> wechat-publisher 的配置一次性搞定，之后就不用再管了。

---

## 新电脑配置指南

如果你的工作流需要自动完成「写文章 → 生图 → 发草稿箱」全流程，换新电脑后按以下步骤配置。

微信长文自动发布的完整流程：

```
kakarot-writer 写文 → 存 md → 生成配图+封面 → 查公网 IP → 发到草稿箱
```

### 1. 安装 skills
将本仓库里的 skill 文件夹复制到对应路径：

| Skill | 复制到 |
|-------|--------|
| `kakarot-writer/` | `~/.claude/skills/kakarot-writer/` |
| `wechat-publisher/` | `~/.codex/skills/wechat-publisher/` |

### 2. 安装 wechat-publisher CLI
```bash
cd ~/.codex/skills/wechat-publisher/tools/wechat-publisher
python3 -m venv venv
venv/bin/pip install .
```

### 3. 配置公众号凭证
创建 `~/.wechat-publisher/.env`：
```
WECHAT_APP_ID=wx你的AppID
WECHAT_APP_SECRET=你的AppSecret
WECHAT_AUTHOR=Kakarot说AI
WECHAT_DEFAULT_COVER_MEDIA_ID=上传封面后获得的media_id
```

> **获取封面 media_id：** 首次使用时，用 `wechat-publisher upload-cover 封面图.jpg` 上传一张封面图，把返回的 media_id 填入。

### 4. 配置生图 API Key
创建 `~/.siliconflow_env`：
```
export SILICONFLOW_API_KEY=你的硅基流动APIKey
```

生图使用硅基流动的 `Tongyi-MAI/Z-Image-Turbo` 模型，每张图约 2-3 秒完成。

### 5. 添加 IP 白名单
首次发布时会报 `40164` 错误并告知当前 IP。去 mp.weixin.qq.com → 开发 → 基本配置 → IP 白名单 添加该 IP，之后即可自动发布。

### 6. 创建草稿目录
```bash
mkdir -p ~/公众号草稿/images
```

配置完成后，对 Claude 说"帮我写篇文章"，即可自动完成写文、生图、发布全流程。

---

## 安装

在 Claude Code 中直接输入：

```
帮我安装这个 skill：https://github.com/Zhangs-11/zs-skills/tree/main/<skill-name>
```

将 `<skill-name>` 替换为 `kakarot-writer`、`fable-writer`、`wechat-publisher`、`aihot`、`life-designer`、`resume-optimizer`、`dating-chat-coach` 或 `system-structure-diagram-skill`。

---

## 快速上手

安装成功后，直接对 Claude 说：

```
帮我写一篇关于大模型价格战的文章
```

Claude 会自动用 kakarot-writer 的风格写出来。如果还想存到公众号：

```
存到公众号
```

Claude 会调用 wechat-publisher 帮你格式化并存入草稿箱。

想查 AI 资讯：

```
今天 AI 圈有什么大事
```

想画架构图：

```
帮我把项目的模块结构画成架构图，和这张图风格一样 [附图]
```
