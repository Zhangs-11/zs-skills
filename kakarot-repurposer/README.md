# kakarot-repurposer

> 多平台不是多套内容，而是同一篇母稿在不同屏幕上换一种讲法。

[![GitHub stars](https://img.shields.io/github/stars/Zhangs-11/zs-skills?style=flat-square)](https://github.com/Zhangs-11/zs-skills)
[![Last commit](https://img.shields.io/github/last-commit/Zhangs-11/zs-skills?style=flat-square)](https://github.com/Zhangs-11/zs-skills/commits/main)
[![License](https://img.shields.io/github/license/Zhangs-11/zs-skills?style=flat-square)](../LICENSE)

kakarot-repurposer 把 `kakarot-writer` 交付的内容母稿作为唯一事实源，再分别按小红书、抖音和B站的阅读或视频节奏组织。事实、案例、核心判断和作者立场不变，标题长度、段落密度、口播节奏、字幕与画面可以适配。

## 安装

```bash
npx skills add Zhangs-11/zs-skills --skill kakarot-repurposer
```

## 你可以这样说

- “把这篇公众号文章转成小红书版。”
- “改成 60 秒抖音口播脚本。”
- “把这篇做成 B站视频稿和专栏版。”
- “一稿多平台，小红书、抖音和B站都给我。”

## 你会得到

- 小红书：标题候选、正文、话题标签与配图建议
- 抖音：一句一行的口播稿、画面/节奏建议与字幕素材
- B站：可原文同步的专栏稿，或保留完整论证的视频稿、分章节与画面建议
- 所有版本共享母稿中的事实、案例、立场、来源与作者声音
- 可选的字幕文件生成脚本

## 前置条件与边界

- [ ] 需要一篇已写好的长文、文章文件或足够完整的正文素材。
- 从零写公众号长文应使用 `kakarot-writer`。
- 发布到微信草稿箱应使用 `wechat-publisher`。
- 改写不能新增原文没有的经历、数据或产品结论。

## Troubleshooting

| 问题 | 解决方法 |
|---|---|
| 结果只是原文缩写 | 明确目标平台和时长，让 Skill 在不改变内容事实的前提下重新组织结构 |
| 口播听起来像书面语 | 要求按真实说话停顿拆句，并朗读检查 |
| 原文信息不完整 | 先补齐事实来源和作者立场，再做分发版本 |
| 不同平台出现了不同结论 | 回到内容母稿，删除派生稿自行新增的观点、案例和作者经历 |

完整平台规范见 [SKILL.md](SKILL.md)。
