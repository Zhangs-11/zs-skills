# human-writing

> 你给 AI 几条观点，它很容易写出一篇句句正确、没有材料、也没有人在说话的长文。

[![GitHub stars](https://img.shields.io/github/stars/Zhangs-11/zs-skills?style=flat-square)](https://github.com/Zhangs-11/zs-skills)
[![Last commit](https://img.shields.io/github/last-commit/Zhangs-11/zs-skills?style=flat-square)](https://github.com/Zhangs-11/zs-skills/commits/main)
[![License](https://img.shields.io/github/license/Zhangs-11/zs-skills?style=flat-square)](../LICENSE)

human-writing 先检查一篇作品靠什么站住，再处理结构、句子和语气。材料不足时，它会研究、追问或缩短，不用假例子和同义改写把三条观点灌成三千字。

它既可以独立写知乎、博客、公众号、人物故事、科普、教程和小说，也可以作为更具体个人写作 Skill 的正文引擎。个人 Skill 负责“谁在说”，human-writing 负责“这篇正文是否真实、自然、值得读完”。

## 安装

```bash
npx skills add Zhangs-11/zs-skills --skill human-writing
```

查看是否可发现：

```bash
npx skills add Zhangs-11/zs-skills --list
```

安装后新开一次 Claude Code、Codex 或其他兼容 Agent Skills 的会话。

## 你可以这样说

- “把这些散乱笔记写成一篇自然的知乎长文，材料不够先告诉我。”
- “重写这篇行业稿，保留事实，删掉机构腔和重复解释。”
- “根据这些采访和时间线写人物故事，不要补不存在的对白。”
- “写一篇短篇小说，人物行动和因果要前后接得上。”

## 它会做什么

1. 区分可靠事实、用户亲历、推断、未知和获准虚构的部分。
2. 检查主要段落是否有动作、数字、原话、失败、代价或来源支撑。
3. 让文章沿着读者自然产生的问题往前走，不靠“更深一层”排队。
4. 保留中文白话的主干、词序、停顿和正常的不确定感。
5. 初稿完成后再检查模型腔、商业黑话、假细节和重复灌水。

## 与个人写作 Skill 配合

例如与 `kakarot-writer` 同时使用时：

```text
kakarot-writer
  确定张硕的作者位置、材料、判断和完整交付
        ↓
human-writing
  生成事实站得住、自然推进的正文
        ↓
kakarot-writer
  个人风格复核、标题、配图和封面
```

个人 Skill 可以覆盖冒号、破折号、对比句和段落节奏等表层规则，不能覆盖事实、来源、用户亲历和现实与虚构边界。

## 前置条件与边界

- [ ] 已安装 Agent Skills CLI，可运行 `npx skills --help` 验证。
- [ ] 非虚构长文尽量提供原始笔记、链接、采访、截图或明确观点。
- [ ] 需要最新事实时允许 Agent 联网研究，并优先使用一手来源。
- [ ] 个人经历缺失时，接受最多三个集中问题；不想补充时应接受更短的成稿。

本 Skill 不替用户创造现实亲历，也不建立长期作者画像。医疗、法律、金融等高风险内容仍需专业来源和相应提醒。

## 目录

```text
kakarot-human-writing/
├── SKILL.md
├── README.md
├── references/
│   ├── forum-prose.md
│   ├── reality.md
│   ├── fiction.md
│   ├── formats.md
│   └── revision.md
└── scripts/
    └── check_prose.py
```

## Troubleshooting

| 问题 | 解决方法 |
|---|---|
| `No valid skills found` | 运行 `npx skills add Zhangs-11/zs-skills --list`，确认名称是 `human-writing` |
| 材料很少却没有直接出长文 | 补充真实经历或来源；不想补充时明确要求缩小题目并写短稿 |
| 与个人文风规则冲突 | 同时启用更具体的个人 Skill，由它覆盖表层文风；事实边界仍以 human-writing 为准 |
| 检查脚本命中个人允许的句式 | 调度模式下把脚本作为提醒，不机械追求零命中 |

## License

MIT。详见 [LICENSE](LICENSE)。
