# wechat-publisher

公众号文章发布工具。配合 `kakarot-writer` 写作 skill 使用，写完后一键格式化并存入微信草稿箱。

## 工作流程

1. 在 Claude Code 中用 kakarot-writer 生成公众号文章
2. 自动保存到本地 markdown
3. 用 `scripts/generate_wechat_images.py` 生成正文图和封面图
4. 把正文占位符替换成 Markdown 图片语法，例如 `![流程图](images/01-rag.png)`
5. 通过 wechat-publisher CLI 上传正文图片、封面图、格式化、调用微信 API
6. 文章自动存入公众号草稿箱

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
| `wechat-publisher create --title "标题" --content-file article.md --cover-file images/cover.png` | 上传封面文件后创建草稿 |
| `wechat-publisher update --media-id "xxx" --title "标题" --content-file article.md` | 更新草稿 |
| `wechat-publisher upload-image photo.jpg` | 上传正文图片 |
| `wechat-publisher upload-cover cover.jpg` | 上传封面图 |

## 生成图片

图片生成由 skill 编排负责，不由发布 CLI 直接调用生图模型。运行时把 SiliconFlow Key 放在环境变量里，不要写进仓库。

```bash
export SILICONFLOW_API_KEY="your_key_here"

python wechat-publisher/scripts/generate_wechat_images.py \
  --article ~/公众号草稿/article.md \
  --title "文章标题" \
  --auto-insert 3
```

默认接口和模型：

- API Base: `https://api.siliconflow.cn/v1`
- Endpoint: `/images/generations`
- Model: `stabilityai/stable-diffusion-xl-base-1.0`

脚本会生成 `images/cover.png`。如果正文里有 `[插图：...]` / `[绘图提示：...]`，会按这些 prompt 生成图片并替换成真实 Markdown 图片；如果没有占位符，会按正文段落自动插入 `--auto-insert` 张配图。

## 图片和链接

- 正文中的本地图片和远程图片会先上传到微信 CDN，再替换成 `mmbiz.qpic.cn` URL。
- 已经是微信 CDN 的图片不会重复上传。
- `[插图：...]` / `[绘图提示：...]` 是写作阶段占位符；发布前必须替换成真实 Markdown 图片，否则命令会失败。
- 正文外链会转换成底部“参考资料”，避免公众号正文里出现不可点击或体验不稳定的外链。

## 摘要和封面

- `WECHAT_DEFAULT_COVER_MEDIA_ID`、`--cover-media-id` 或 `--cover-file` 必须存在，否则会提前报错。
- 不传 `--digest` 时，工具会从第一段有效正文自动提取 120 字以内摘要。
- `--source-url` 会写入微信草稿的原文链接字段。
- `--show-cover-pic` 会在正文顶部显示封面图；默认不显示。

## 测试

```bash
cd tools/wechat-publisher
.venv/bin/python -m unittest discover -s tests -v

# 回到仓库根目录后测试 skill 图片生成脚本
cd ../..
tools/wechat-publisher/.venv/bin/python -m unittest tests/test_generate_images_script.py -v
```
