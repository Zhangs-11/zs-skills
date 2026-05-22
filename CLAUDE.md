# zs-skills 使用说明

本 repo 包含 Kakarot 的 Claude Code Skills 合集。每次在新电脑上使用时，按以下步骤配置才能正常工作。

## 技能安装路径

| Skill | 安装位置 |
|-------|---------|
| kakarot-writer | `~/.claude/skills/kakarot-writer/` |
| fable-writer | `~/.claude/skills/fable-writer/` |
| wechat-publisher | `~/.codex/skills/wechat-publisher/` |
| aihot | `~/.claude/skills/aihot/` |

技能文件夹内不包含 `.git`，直接从本 repo 复制过去即可。

## 公众号自动发布工作流

当用户说"写一篇公众号文章"或类似意图时，自动执行以下流程：

### Step 1: 写作
调用 kakarot-writer skill 生成文章，严格遵循其风格规范。

### Step 2: 保存
将 `.md` 文件保存到 `~/公众号草稿/` 目录。

### Step 3: 生图
用 SiliconFlow 的 `Tongyi-MAI/Z-Image-Turbo` 模型生成正文配图（3张）+ 封面图。

API Key 从 `~/.siliconflow_env` 加载（source 该文件后会 export `SILICONFLOW_API_KEY`）。

生图脚本路径：
```
.codex/skills/wechat-publisher/scripts/generate_wechat_images.py
```

注意：需使用 curl 调 API + 下载图片（Python 3.13 urllib SSL 连阿里云 S3 有兼容问题）。

图片保存到 `~/公众号草稿/images/`，并自动插入文章正文。

### Step 4: 查 IP
```
curl -s ip.sb
```

### Step 5: 发布
调 wechat-publisher CLI 发到草稿箱：
```
.codex/skills/wechat-publisher/tools/wechat-publisher/venv/bin/wechat-publisher create \
  --title "文章标题" \
  --content-file ~/公众号草稿/文件名.md \
  --cover-file ~/公众号草稿/images/cover.png \
  --show-cover-pic \
  --digest "摘要"
```

### Step 6: 汇报
以表格形式告知用户每一步的状态。

- **成功** → 告知 media_id
- **失败 40164（IP 白名单）** → 告知当前 IP，让用户去微信后台添加白名单
- **其他失败** → 告知具体原因和解决步骤

## 新电脑初始化清单

### 1. 安装 skills
将本 repo 中的技能文件夹复制到对应安装路径。

### 2. 安装 wechat-publisher CLI 依赖
```bash
cd .codex/skills/wechat-publisher/tools/wechat-publisher
python3 -m venv venv
venv/bin/pip install .
```

### 3. 配置 WeChat 凭证
创建 `~/.wechat-publisher/.env`，内容模板：
```
WECHAT_APP_ID=wx你的AppID
WECHAT_APP_SECRET=你的AppSecret
WECHAT_AUTHOR=Kakarot说AI
WECHAT_DEFAULT_COVER_MEDIA_ID=你的封面media_id
```

### 4. 配置 SiliconFlow API Key
创建 `~/.siliconflow_env`：
```
export SILICONFLOW_API_KEY=你的硅基流动APIKey
```

### 5. 添加微信 IP 白名单
去 mp.weixin.qq.com → 开发 → 基本配置 → IP 白名单，添加当前电脑的公网 IP。

### 6. 创建草稿目录
```bash
mkdir -p ~/公众号草稿/images
```

## 注意

- 本 CLAUDE.md 中所有 `你的xxx` 占位符需替换为真实值，凭证信息不进 git
- WeChat 封面 media_id 首次需先用 `wechat-publisher upload-cover` 上传封面图获取
