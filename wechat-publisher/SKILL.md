---
name: wechat-publisher
description: |
  公众号文章发布工具。当用户说"存到公众号"、"发布到公众号"、"发到草稿箱"、"推到公众号"、"写到公众号"时触发。配合 kakarot-writer skill 使用：先用 kakarot-writer 风格生成 markdown 文章 → 用 wechat-publisher CLI 格式化并存入微信草稿箱。也支持纯 markdown 文件直接发布。

  触发词：存到公众号、发布到公众号、发到草稿箱、推到公众号、写到公众号、发公众号、wechat publish

  不触发情况：纯写作不涉及发布、不需要存草稿箱的情况。
---

# wechat-publisher 公众号发布工具

作者在「Kakarot说AI」公众号写文章，写完后需要一键存到微信草稿箱，不用手动复制粘贴。

## 架构概览

```
kakarot-writer skill 生成 markdown 文章
       │
       ▼
scripts/generate_wechat_images.py → 生成正文图 + 封面图
       │
       ▼
wechat-publisher create --title "xxx" --content-file xxx.md --cover-file images/cover.png
       │
       ├─ formatter.py  →  Markdown → 微信兼容 HTML
       ├─ token.py      →  access_token 缓存管理
       ├─ client.py     →  微信 API HTTP 调用
       └─ 微信服务器     →  草稿箱 +1
```

## 安装

仅首次安装时执行。如果用户已经装过，跳过这一步。

### 1. 安装 Python 包

```bash
cd tools/wechat-publisher
python3 -m venv venv
venv/bin/pip install -e .
```

### 2. 创建配置文件

在 `~/.wechat-publisher/.env` 中写入：

```bash
WECHAT_APP_ID=wx你的AppID
WECHAT_APP_SECRET=你的AppSecret
WECHAT_AUTHOR=Kakarot说AI
WECHAT_DEFAULT_COVER_MEDIA_ID=你的封面media_id
```

**注意：** 密钥在用户本地 `~/.wechat-publisher/.env`，不在仓库里。`WECHAT_DEFAULT_COVER_MEDIA_ID` 先用 `wechat-publisher upload-cover` 上传一张封面图获取 media_id 再填入。

### 3. 添加 PATH

如果 `wechat-publisher` 命令找不到，用全路径：

```bash
# 或建立软链接
ln -sf $(pwd)/tools/wechat-publisher/venv/bin/wechat-publisher ~/.local/bin/wechat-publisher
```

### 4. IP 白名单

微信 API 要求调用方的公网 IP 在公众号后台白名单中。如果遇到 `40164` 错误，告诉用户当前 IP 并让用户去 mp.weixin.qq.com → 开发 → 基本配置 → IP 白名单 添加。

## 工作流

当用户说"写一篇 XX 文章存到公众号"时，必须按以下步骤执行：

### 第一步：写作
调用 kakarot-writer skill 生成 markdown 文章。

**标题策略：制造信息缺口（curiosity gap），让人想点进来。** 问句、悬念陈述句、反差句都可以，不限形式。例如：

- ✅ "GitHub 25万星标的神级插件，为什么大家都在卸载它"（反差）
- ✅ "跑了一下马斯克的编程工具，我的SSH密钥没了"（悬念）
- ✅ "传统RAG真要完？我花了两天研究PageIndex和Wiki，发现事情没那么简单"（问句）

标题应该：暗示文章有独家信息/真实体验 + 保持克制不浮夸 + 让普通人也看得懂。

在文章中需要配图的位置，使用以下格式插入占位标记：

```markdown
[插图：图片内容描述]
[绘图提示：可复制的英文 prompt，适合 Midjourney / DALL-E / 即梦 等生图工具]
```

例：
```markdown
[插图：传统RAG工作流程图]
[绘图提示：A clean technical diagram showing the classic RAG pipeline, flat design with blue and white color scheme, modern minimalist style.]
```

这告诉用户两个信息：**哪里需要配图**、**用什么 prompt 生成图片**。

**绘图提示的写法（重要）：**
- **有创意，用视觉比喻概括语义**，不要把正文文字照搬进去。prompt 描述的是「一个画面/场景」，不是「这段话写了啥」。
- **纯英文**。中文一旦进 prompt，生图模型 Z-Image-Turbo 会把中文直接画到图上，且常带错别字。
- **画面里不要出现任何文字**（prompt 末尾脚本会自动追加强力的「无文字」约束 + negative_prompt，你自己写的时候也别要求图上有字）。
- 例（解释「海量上下文被收束成清晰的推理」）：`A vast turbulent cloud of glowing particles funneling through a sleek device into one calm focused beam of blue light, flat editorial illustration, blue palette, no text`

### 第二步：保存
将文章保存到 `~/公众号草稿/` 目录。

### 第三步：生成图片

发布前必须先运行图片生成脚本。脚本使用 SiliconFlow 图片生成接口，默认模型是 `Tongyi-MAI/Z-Image-Turbo`。

如果文章包含 `[插图：...]` / `[绘图提示：...]`，脚本会按这些 prompt 生成对应正文图（**优先走这条**，因为 prompt 是你手写的、有创意）。如果文章没有占位符，脚本会按正文段落自动插入 3 张配图，并生成封面图——auto 兜底通道会先用对话模型（`deepseek-ai/DeepSeek-V3`）把中文段落转成英文视觉概念再生图，**绝不把中文塞进画面**，从根上避免图上出现原文和错别字。封面也走概念化（不再把标题原文塞进 prompt，并去掉「杂志封面」这类诱导加标题字的措辞，缩写如 AI/GPT 也会被剔除）。封面对文字最敏感，**要最稳就手动传 `--cover-prompt "英文创意概念"`**。

**图片目录**：每篇文章的图存在以文件名命名的独立子目录 `images/<文章名>/` 下（封面 `cover.png`、正文 `01-image.png`…），多篇之间不会再互相覆盖。

> 所有生图 prompt 末尾都会自动叠加统一创作方向（视觉比喻、蓝色调、画面零文字）+ `negative_prompt` 负向词，进一步压制文字渲染。

**密钥只放在运行环境中，不写入仓库或文章文件。**

```bash
export SILICONFLOW_API_KEY="用户提供的 SiliconFlow API Key"

python wechat-publisher/scripts/generate_wechat_images.py \
  --article ~/公众号草稿/文件名.md \
  --title "文章标题" \
  --auto-insert 3
```

脚本会：

1. 调用 `https://api.siliconflow.cn/v1/images/generations` 生成图片。
2. 立即下载图片到 `~/公众号草稿/images/<文章名>/`，不要只保存临时 URL。
3. 把正文占位符替换成真实 Markdown 图片；没有占位符时，自动在正文段落后插入配图，例如 `![配图1](images/<文章名>/01-image.png)`。
4. 生成封面图 `images/<文章名>/cover.png`。

### 第四步：尝试发布

`wechat-publisher` 会自动上传正文 Markdown 图片到微信 CDN。封面图用 `--cover-file` 上传成微信永久素材，再用返回的 `media_id` 创建草稿。已经是 `mmbiz.qpic.cn` 的图片不会重复上传。

```bash
# 检查当前公网 IP
curl -s ip.sb

# 尝试发布
wechat-publisher create \
  --title "文章标题" \
  --content-file ~/公众号草稿/文件名.md \
  --cover-file ~/公众号草稿/images/cover.png \
  --digest "120字以内摘要"
```

### 第五步：结果处理

**成功** → 告知用户 `SUCCESS: Draft created (media_id=xxx)`

**失败（40164 IP白名单）** → 告诉用户当前IP，让用户去微信后台添加白名单，然后重新运行发布命令

**失败（其他错误）** → 根据错误信息处理

## 命令参考

### create — 创建草稿

```bash
# 从文件
wechat-publisher create --title "标题" --content-file article.md

# 自动上传封面文件
wechat-publisher create --title "标题" --content-file article.md --cover-file images/cover.png

# 从管道
cat article.md | wechat-publisher create --title "标题"
```

### update — 更新现有草稿

```bash
wechat-publisher update --media-id "xxx" --title "新标题" --content-file article.md
```

### upload-image — 上传正文图片（返回 CDN URL）

```bash
wechat-publisher upload-image photo.jpg
# → SUCCESS: Image uploaded → http://mmbiz.qpic.cn/...
```

### upload-cover — 上传封面图（返回 media_id）

```bash
wechat-publisher upload-cover cover.jpg
# → SUCCESS: Cover uploaded (media_id=xxx)
```

## 样式机制

`formatter.py` 自动将 markdown 转为微信内联样式 HTML：

| 元素 | 效果 |
|------|------|
| 正文段落 | 16px, 深灰, 行距 1.85 |
| `===高亮===` | 蓝色渐变底强调 |
| `==注意小句==` | 仅把字变成主题蓝（无底色、不加粗），标关键句用，代替加粗 |
| `> 引用` | 💡 蓝色竖线卡片 |
| `## 二级标题` | 左竖线小标题：蓝色左竖线 + 同色蓝字 + 加粗，字号与正文一致（前置图标，标题没带 emoji 会自动补 🔹） |
| `### 三级标题` | 同款，竖线略细 |
| `---` | `· · ·` 分隔符 |
| `` `代码` `` | 浅灰底圆角代码 |
| ```代码块``` | 深色圆角代码块 |
| `**加粗**` | 700 字重深色 |
| `*斜体*` | 斜体 |
| 表格 | 微信兼容表格样式 |
| 外链 | 正文标注序号，底部生成参考资料 |

## 内容质检规则

高流量 AI 公众号文章发布前要做四项检查：

1. 标题有具体对象、反常识或真实体验，不使用空泛震惊体。
2. 前三行必须交代“发生了什么”和“为什么值得读”。
3. 每 3-5 段至少有一个人为加粗的判断句，方便扫读；不要依赖工具自动加粗。
4. 配图必须服务理解，且**图里不要出现任何文字**（生图模型画中文会出错别字）。优先用视觉比喻/概念图传达意思，绘图提示用纯英文手写、有创意，不要把正文照搬进 prompt。

## 常见错误

| 错误 | 原因 | 处理 |
|------|------|------|
| 40164 | IP 不在白名单 | 获取当前 IP，让用户添加白名单 |
| 40007 invalid media_id | 封面 media_id 无效或为空 | 上传封面图获取正确的 media_id |
| 40001 | token 过期或无效 | 会自动刷新，持久失败检查 appsecret 是否正确 |
| 45009 | 接口频率超限 | 会自动重试 |

## 发布前失败保护

- 如果缺少封面，命令会失败并提示配置 `WECHAT_DEFAULT_COVER_MEDIA_ID`、传 `--cover-media-id`，或传 `--cover-file`。
- 如果正文仍包含 `[插图：...]` / `[绘图提示：...]`，命令会失败，防止半成品进入草稿箱。
- 如果遇到 40164，命令会提示去微信后台添加当前公网 IP 白名单。
