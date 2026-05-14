# wechat-publisher

公众号文章发布工具。配合 `kakarot-writer` 写作 skill 使用，写完后一键格式化并存入微信草稿箱。

## 工作流程

1. 在 Claude Code 中用 kakarot-writer 生成公众号文章
2. 自动保存到本地 markdown
3. 把正文图片写成 Markdown 图片语法，例如 `![流程图](images/rag.png)`
4. 通过 wechat-publisher CLI 上传正文图片、格式化、调用微信 API
5. 文章自动存入公众号草稿箱

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
| `wechat-publisher create --title "标题" --content-file article.md --digest "摘要"` | 创建草稿并指定信息流摘要 |
| `wechat-publisher create --title "标题" --content-file article.md --cover-media-id "xxx"` | 用指定封面创建草稿 |
| `wechat-publisher update --media-id "xxx" --title "标题" --content-file article.md` | 更新草稿 |
| `wechat-publisher upload-image photo.jpg` | 上传正文图片 |
| `wechat-publisher upload-cover cover.jpg` | 上传封面图 |

## 图片和链接

- 正文中的本地图片和远程图片会先上传到微信 CDN，再替换成 `mmbiz.qpic.cn` URL。
- 已经是微信 CDN 的图片不会重复上传。
- `[插图：...]` / `[绘图提示：...]` 是写作阶段占位符；发布前必须替换成真实 Markdown 图片，否则命令会失败。
- 正文外链会转换成底部“参考资料”，避免公众号正文里出现不可点击或体验不稳定的外链。

## 摘要和封面

- `WECHAT_DEFAULT_COVER_MEDIA_ID` 或 `--cover-media-id` 必须存在，否则会提前报错。
- 不传 `--digest` 时，工具会从第一段有效正文自动提取 120 字以内摘要。
- `--source-url` 会写入微信草稿的原文链接字段。
- `--show-cover-pic` 会在正文顶部显示封面图；默认不显示。

## 测试

```bash
cd tools/wechat-publisher
.venv/bin/python -m unittest discover -s tests -v
```
