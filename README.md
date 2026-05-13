# zs-skills

Kakarot 的个人 Claude Code Skill 合集。

帮你写公众号文章、查 AI 资讯、画架构图，一条龙搞定。

---

## 技能一览

| Skill | 能做什么 | 怎么触发（对 Claude 说） |
|-------|---------|------------------------|
| **kakarot-writer** | 按「Kakarot说AI」的风格写公众号长文 | "帮我写篇文章"、"写稿子"、"按我的风格写" |
| **wechat-publisher** | 把写好的文章一键存到微信草稿箱 | "存到公众号"、"发到草稿箱"、"推到公众号" |
| **aihot** | 查 AI 圈今天发生了什么 | "AI 圈"、"AI 日报"、"今天 AI 有什么新闻" |
| **system-structure-diagram** | 按参考图风格生成系统结构图 | "画系统架构图"、"按这个样式画图" |

> 两个配合使用效果最好：`kakarot-writer` 写文章 → `wechat-publisher` 存到公众号，一条龙。

---

## 前置条件

每个 skill 需要的东西都在这里，**没有额外依赖的就不需要装任何东西**。

| Skill | 需要准备 |
|-------|---------|
| **kakarot-writer** | 什么都不用装。安装后直接对 Claude 说"帮我写篇文章"就行。 |
| **aihot** | 什么都不用装。安装后直接问"AI 圈有什么"就行。底层调公开 API，不需要 API Key。 |
| **system-structure-diagram** | 需要装好 [Inkscape](https://inkscape.org/release/)（SVG 转 PNG 用）。macOS: `brew install inkscape`。Windows/Linux 去官网下载。 |
| **wechat-publisher** | 需要准备两样东西：<br>1. **Python 3.12+**（macOS: `brew install python@3.13`）<br>2. **公众号 AppID 和 AppSecret**（去 mp.weixin.qq.com → 开发 → 基本配置 获取）<br>3. **公网 IP 加入白名单**（装好后运行时报错会告诉你当前 IP，去后台加一下就行） |

> wechat-publisher 的配置一次性搞定，之后就不用再管了。

---

## 安装

在 Claude Code 中直接输入：

```
帮我安装这个 skill：https://github.com/Zhangs-11/zs-skills/tree/main/<skill-name>
```

将 `<skill-name>` 替换为 `kakarot-writer`、`wechat-publisher`、`aihot` 或 `system-structure-diagram-skill`。

---

## 快速上手

安装成功后，直接对 Claude 说：

```
帮我写一篇关于大模型价格战的文章
```

Claude 会自动用 kakarot-writer 的风格写出来。如果还想存到公众号：

```
存到公众号
```

Claude 会调用 wechat-publisher 帮你格式化并存入草稿箱。

想查 AI 资讯：

```
今天 AI 圈有什么大事
```

想画架构图：

```
帮我把项目的模块结构画成架构图，和这张图风格一样 [附图]
```
