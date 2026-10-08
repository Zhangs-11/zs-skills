# 幼儿园教案与可爱课件

为学前教育作业和幼儿园课堂制作一套 Word 教案与可爱 PPT。教学目标写成幼儿能够表现出的学习结果，过程标题写清活动和目的，课件用大图、少字及课堂提问引导幼儿参与。

[![Skill quality](https://img.shields.io/github/actions/workflow/status/Zhangs-11/zs-skills/skill-quality.yml?branch=main)](https://github.com/Zhangs-11/zs-skills/actions/workflows/skill-quality.yml) [![Last commit](https://img.shields.io/github/last-commit/Zhangs-11/zs-skills)](https://github.com/Zhangs-11/zs-skills/commits/main) [![License MIT](https://img.shields.io/badge/license-MIT-blue.svg)](../LICENSE)

![大班科学活动会变的影子课件示例](assets/lesson-cover.png)

图为实际生成的《会变的影子》课件封面。每次使用会根据课题重新设计内容和插图，示例图片不作为固定模板。

```bash
npx skills add Zhangs-11/zs-skills --skill preschool-lesson-kit
```

## 使用

安装后新开一次会话，可以直接说：

- “参考这个教案另选课题，帮我做一套教案和PPT，课件要可爱。”
- “做一节小班认识树叶的活动，重点写教学目标，PPT给幼儿看。”
- “把教学过程标题改成一眼能看出做什么、目的是什么的写法。”

也可以明确调用 `$preschool-lesson-kit`。

## 会得到什么

| 材料 | 内容 |
|---|---|
| Word 教案 | 班级与时长、教学目标、准备、活动过程、评价和延伸，按作业要求排版 |
| PPT 课件 | 适合幼儿观看的图片、简短提问和操作任务，备注提供教师讲解与操作条件 |

教案过程标题示例：“移动手电筒，探索影子大小的变化”。对应PPT可以写：“只移动手电筒”，再提醒“纸偶和屏幕保持不动”。

未另行指定时，Word采用1.5倍行间距，主标题黑体四号加粗居中，章节标题宋体四号加粗顶格，正文宋体小四并首行缩进2字符。小班、中班、大班的目标与任务分别设计，单套材料明确一个班级。

## 前置条件与安装验证

- [ ] 安装[Node.js](https://nodejs.org/)，运行 `node --version` 和 `npx --version` 确认命令可用。
- [ ] 在支持 Agent Skills 的工具中安装本 Skill；安装后运行 `npx skills add Zhangs-11/zs-skills --list`，确认列表中有 `preschool-lesson-kit`。
- [ ] 制作文件时需要文档和演示文稿制作能力。Codex中可使用 `documents:documents` 与 `presentations:Presentations`；在其他工具中使用当前可用的对应能力，按其文档配置依赖并验证导出与渲染。
- [ ] 制作原创插图时需要可用的图像生成工具，例如 `imagegen`；也可使用经过核查、来源可追溯的现有图片。

本 Skill 不包含固定课件模板或整套绘图程序，文件制作由当前环境的工具执行。只改文字或标题时，无需生成新插图。

## 常见问题

| 问题 | 处理方法 |
|---|---|
| 安装后没有发现 Skill | 新开会话，确认安装到了当前工具读取的目录，再运行上面的列表命令 |
| Word预览缺少中文 | 检查字体是否可用以及渲染器能否发现中文字体，修复映射后重新渲染 |
| PPT文字多或像成人汇报 | 每页只保留一个观察、问题或任务，把完整教师讲解放入备注 |
| 标题只写“找一找”“试一试” | 在教案标题中补出具体活动和目的，PPT保留适合幼儿的简短说法 |

资料参考优先采用教育部门的指导文件和具体课题的原始材料。插图与科学结论需核查；成品未经真实课堂试教时，不声称教学效果已经验证。上传到学校或发布到外部平台须有本次明确授权。

## English

Create a kindergarten lesson plan in Word and a matching, cute classroom presentation. Learning objectives describe observable child behavior. Lesson-plan headings state both the activity and its purpose. Slides use large visuals and short prompts, with teacher guidance in speaker notes. Each set targets one age group and is visually checked before delivery.

Install with the command above, then ask: “Use this reference to create one kindergarten lesson plan and a cute classroom PPT for a new topic.”

The workflow uses the document, presentation, image-generation, and rendering capabilities available in the host environment. It does not include a fixed theme or claim classroom-tested effectiveness.

采用本仓库的 [MIT License](../LICENSE)。示例插图由图像生成工具制作。
