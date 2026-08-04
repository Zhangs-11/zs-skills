# system-structure-diagram

> 项目模块是真实的，参考图的版式也很明确，最容易翻车的却是连线、间距和字体这些细节。

一个适用于 Codex 及其他 Agent Skills 兼容工具的 skill，用于按参考图片的样式生成系统结构图、功能结构图和模块树图片。

它适合这类需求：

- “按这张示意图的格式，帮我画系统结构图”
- “保持背景、框线、连线和字体风格不变，只替换内容”
- “输出一份可继续微调的 SVG，再导出 PNG”

## 功能

- 根据真实项目结构提取角色和模块层级
- 复刻参考图的背景、框体、连线和排版风格
- 优先生成可精确控制的 SVG
- 导出 PNG 供预览和分享
- 支持继续微调：
  - 连线断开
  - 多余尾线
  - 竖排文字居中
  - 文字超框
  - 字体和字重不一致

## 安装

```bash
npx skills add Zhangs-11/zs-skills --skill system-structure-diagram
```

安装后重启或新开一次 Agent 会话。

## 使用方式

推荐显式调用：

```text
使用 $system-structure-diagram，参考我上传的图片，按同样的背景、框线、连线和字体风格，生成我项目的系统结构图，并输出 SVG 和 PNG。
```

也可以英文调用：

```text
Use $system-structure-diagram to create a system structure diagram based on this reference image and replace the content with real project modules.
```

说明：

- 它不是 `/xxx` 这种 slash command。
- 最稳的方式是在提示词里直接写 `$system-structure-diagram`。
- 如果你的请求本身就很明确，Codex 也可能自动触发这个 skill。

## 仓库结构

```text
system-structure-diagram/
  SKILL.md
  agents/
    openai.yaml
```

## 示例场景

- 系统结构图
- 论文中的功能模块图
- 答辩 PPT 中的模块树图
- 根据现有项目代码自动整理出来的角色-功能结构图

## License

MIT

## Troubleshooting

| 问题 | 解决方法 |
|---|---|
| 图中模块与项目不符 | 先读取路由、菜单、控制器和模块目录，不凭参考图猜内容 |
| PNG 与 SVG 排版不一致 | 固定画布尺寸与字体，修改 SVG 后重新导出 PNG |
| 竖排文字超框或连线有尾巴 | 按框体中心重算文字坐标，并让分支线在最后一个子框中心收口 |
