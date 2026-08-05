# kakarot-writer

> 不是给文章撒几句口头禅，而是把「谁在说、凭什么说、说完交付什么」变成一套稳定工作流。

[![GitHub stars](https://img.shields.io/github/stars/Zhangs-11/zs-skills?style=flat-square)](https://github.com/Zhangs-11/zs-skills)
[![Last commit](https://img.shields.io/github/last-commit/Zhangs-11/zs-skills?style=flat-square)](https://github.com/Zhangs-11/zs-skills/commits/main)
[![License](https://img.shields.io/github/license/Zhangs-11/zs-skills?style=flat-square)](../LICENSE)

`kakarot-writer` 是张硕（Kakarot）的个人长文总调度 Skill。它负责作者位置、选题判断、真实材料、个人风格、标题、配图、封面和最终交付；正文由通用的 [`human-writing`](../kakarot-human-writing/) 生成，再经过个人风格复核。

成稿以公众号首发为基准，同时作为知乎、博客、掘金、小红书、抖音和B站的唯一内容母稿。长文平台可以原文同步；短图文与视频只做形态适配，不另起观点和素材。

![使用官方真实素材生成的公众号封面示例](docs/assets/cover-example.png)

## 安装

建议同时安装个人调度和通用正文引擎：

```bash
npx skills add Zhangs-11/zs-skills --skill kakarot-writer human-writing
```

如果当前 CLI 版本一次只接受一个 Skill，分别执行两次即可。

## 你可以这样说

- “帮我写篇文章，主题是刚入职第一个月怎么过，这是我的经历和笔记。”
- “根据这个产品 brief 写一篇文章，按我的风格完整交付。”
- “把这份 PDF 和采访记录整理成长文，事实不够就先缩小题目。”
- “按我的风格续写这篇稿子，正文不要为不同平台重写。”

“帮我写篇文章”默认不是只交一段正文，而是一套可发布成品：推荐标题与备选标题、Markdown 正文、截图与来源清单、正文配图安排、`21:9` 主封面、`1:1` 分享封面和跨平台通用尾部。

## 工作流

```text
kakarot-writer
  确定作者位置、材料、核心判断和文章原型
        ↓
human-writing
  生成事实站得住、自然推进的正文
        ↓
kakarot-writer
  个人风格复核、标题、截图、配图和双尺寸封面
        ↓
同一篇内容母稿
  公众号首发，并原文同步到知乎、博客、掘金和B站专栏
        ↓
kakarot-repurposer
  派生小红书、抖音和B站视频形态稿，不改变事实与观点
```

个人风格主要从两篇真实文章提炼：以《实习了两年的应届生，想和刚入职的你聊聊，新公司第一个月该怎么过？》校准经验与方法写法，以《二十多岁，为什么我们活成了“成年的未成年人”》补充情绪、代际处境和公共议题写法。它学习的是作者位置和表达机制，不复制句子，也不会把“应届生”等旧状态固化为永久人设。

## 默认封面策略

如已安装 `guizang-social-card-skill`，默认使用它的 B 方案，从产品官网、官方文档、公告、GitHub 等真实素材制作封面。`21:9` 主封面和 `1:1` 分享封面分别排版，不机械裁切。

只有环境里找不到专用封面 Skill 时，才回退到 AI 图片，并明确说明发生了回退。

## 前置条件与边界

- [ ] 安装 `human-writing`，作为正文生成引擎。
- [ ] 提供链接、PDF、brief、原始笔记或真实经历；材料越完整，文章越可靠。
- [ ] 如需默认的真实素材封面，安装 `guizang-social-card-skill`。
- [ ] 文章中的亲历、采访、数据和测试结果必须有真实依据。

生成完整成品不等于发布。只有用户明确说“存到公众号”“发到草稿箱”或“发布”时，才交给对应发布工具写入外部系统。小红书、抖音和B站视频等需要改变呈现形态的内容交给 `kakarot-repurposer`，但始终使用当前母稿的事实、观点和素材。

## Troubleshooting

| 问题 | 解决方法 |
|---|---|
| 正文仍有明显模型腔 | 确认同时安装了 `human-writing`，并补充真实动作、代价、失败和判断 |
| 作者被写成固定的“应届生” | 只把用户本次提供或当前资料确认的职业阶段写进文章 |
| 各平台观点和素材逐渐不一致 | 把 Markdown 母稿作为唯一内容源；派生稿只改变长度、节奏、画面和平台元数据 |
| 封面像抽象 AI 概念图 | 安装 `guizang-social-card-skill`，使用 B 方案抓取真实素材 |
| 标题比正文结论更强 | 降低标题承诺，或补足能兑现标题的证据 |

完整规则见 [SKILL.md](SKILL.md) 和 [references/](references/)。

## License

MIT。详见 [LICENSE](LICENSE)。
