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
wechat-publisher create --title "xxx" --content-file xxx.md
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

**标题策略：使用问句形式作为标题。** 问句能制造好奇缺口（curiosity gap），吸引读者点击。例如：

- ❌ "RAG不会被替代，它只是换了个马甲"
- ✅ "传统RAG真要完？我花了两天研究PageIndex和Wiki，发现事情没那么简单"

标题应该：用问句开头 + 暗示文章有独家信息/真实体验 + 保持克制不浮夸。

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

### 第二步：保存
将文章保存到 `~/公众号草稿/` 目录。

### 第三步：尝试发布

发布前必须把 `[插图：...]` / `[绘图提示：...]` 占位符替换为真实 Markdown 图片：

```markdown
![传统RAG工作流程图](images/rag-flow.png)
```

`wechat-publisher` 会自动上传 Markdown 图片到微信 CDN。已经是 `mmbiz.qpic.cn` 的图片不会重复上传。

```bash
# 检查当前公网 IP
curl -s ip.sb

# 尝试发布
wechat-publisher create --title "文章标题" --content-file ~/公众号草稿/文件名.md --digest "120字以内摘要"
```

### 第四步：结果处理

**成功** → 告知用户 `SUCCESS: Draft created (media_id=xxx)`

**失败（40164 IP白名单）** → 告诉用户当前IP，让用户去微信后台添加白名单，然后重新运行发布命令

**失败（其他错误）** → 根据错误信息处理

## 命令参考

### create — 创建草稿

```bash
# 从文件
wechat-publisher create --title "标题" --content-file article.md

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
| `> 引用` | 💡 蓝色竖线卡片 |
| `## 标题` | 蓝色左竖线装饰 |
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
4. 配图必须服务理解：流程图、对比表、架构图、截图优先，纯氛围图少用。

## 常见错误

| 错误 | 原因 | 处理 |
|------|------|------|
| 40164 | IP 不在白名单 | 获取当前 IP，让用户添加白名单 |
| 40007 invalid media_id | 封面 media_id 无效或为空 | 上传封面图获取正确的 media_id |
| 40001 | token 过期或无效 | 会自动刷新，持久失败检查 appsecret 是否正确 |
| 45009 | 接口频率超限 | 会自动重试 |

## 发布前失败保护

- 如果缺少封面 `media_id`，命令会失败并提示配置 `WECHAT_DEFAULT_COVER_MEDIA_ID` 或传 `--cover-media-id`。
- 如果正文仍包含 `[插图：...]` / `[绘图提示：...]`，命令会失败，防止半成品进入草稿箱。
- 如果遇到 40164，命令会提示去微信后台添加当前公网 IP 白名单。
