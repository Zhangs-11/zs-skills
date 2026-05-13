# wechat-publisher

公众号文章发布工具。配合 `kakarot-writer` 写作 skill 使用，写完后一键格式化并存入微信草稿箱。

## 工作流程

1. 在 Claude Code 中用 kakarot-writer 生成公众号文章
2. 自动保存到本地 markdown
3. 通过 wechat-publisher CLI 格式化 + 调用微信 API
4. 文章自动存入公众号草稿箱

## 快速开始

```bash
# 1. 安装
cd tools/wechat-publisher
python3 -m venv venv
venv/bin/pip install -e .

# 2. 配置
# 编辑 ~/.wechat-publisher/.env，填入 AppID 和 AppSecret

# 3. 上传封面图
wechat-publisher upload-cover cover.jpg
# 将返回的 media_id 填入 .env 的 WECHAT_DEFAULT_COVER_MEDIA_ID
```

IP 白名单：登录 mp.weixin.qq.com → 开发 → 基本配置 → IP 白名单，添加当前公网 IP。

## 命令

| 命令 | 用途 |
|------|------|
| `wechat-publisher create --title "标题" --content-file article.md` | 创建草稿 |
| `wechat-publisher update --media-id "xxx" --title "标题" --content-file article.md` | 更新草稿 |
| `wechat-publisher upload-image photo.jpg` | 上传正文图片 |
| `wechat-publisher upload-cover cover.jpg` | 上传封面图 |
