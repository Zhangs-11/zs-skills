# zs-skills

[English](README.md) | [简体中文](README.zh-CN.md)

> Think through the strongest case on both sides before writing a WeChat article, tracking AI news, diagnosing a problem, reviewing code, briefing a meeting, or drawing a system diagram—without teaching the AI each workflow from scratch.

<p align="center">
  <a href="https://github.com/Zhangs-11/zs-skills/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/Zhangs-11/zs-skills?style=for-the-badge&logo=github" /></a>
  <a href="https://github.com/Zhangs-11/zs-skills/network/members"><img alt="Forks" src="https://img.shields.io/github/forks/Zhangs-11/zs-skills?style=for-the-badge&logo=github" /></a>
  <a href="https://github.com/Zhangs-11/zs-skills/issues"><img alt="Issues" src="https://img.shields.io/github/issues/Zhangs-11/zs-skills?style=for-the-badge&logo=github" /></a>
  <a href="https://github.com/Zhangs-11/zs-skills/commits/main"><img alt="Last commit" src="https://img.shields.io/github/last-commit/Zhangs-11/zs-skills?style=for-the-badge&logo=git" /></a>
  <a href="https://github.com/Zhangs-11/zs-skills/actions/workflows/skill-quality.yml"><img alt="Skill quality" src="https://img.shields.io/github/actions/workflow/status/Zhangs-11/zs-skills/skill-quality.yml?branch=main&style=for-the-badge&label=skill%20quality" /></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge" /></a>
</p>

This repository is a collection of primarily Chinese-language skills for Claude Code, Codex, and other Agent Skills-compatible tools. Each skill keeps its triggers, workflow, boundaries, and supporting resources in a self-contained directory and can be invoked with natural language after installation.

```bash
npx skills add Zhangs-11/zs-skills
```

## 23 installable skills

| Skill | What it solves | Example prompt |
|---|---|---|
| [ai-hot-picker](ai-hot-picker/) | Selects creation-worthy topics from today's AI news | “What AI topic should I write about today?” |
| [aihot](aihot/) | Retrieves the latest AI briefings, releases, papers, and industry news | “What happened in AI today?” |
| [change-meeting-brief](change-meeting-brief/) | Compresses a requirement or PR into a 20–40 second change briefing | “Only cover the problem, the old behavior, and the fix.” |
| [clarify-before-action](clarify-before-action/) | Investigates and clarifies context, requirements, pain points, and acceptance criteria before complex work starts | “Do not change anything yet. Ask one question at a time, then act after I confirm.” |
| [dating-chat-coach](dating-chat-coach/) | Helps with replies, moving to WeChat, invitations, and safety when dating or meeting someone online | “She replied with this. What should I say next?” |
| [deep-research](deep-research/) | Studies an unfamiliar subject through historical development, comparison, and fact-checking | “Research how it got here, how it differs from alternatives, and where it may go next.” |
| [diagnose-and-explain](diagnose-and-explain/) | Diagnoses technical, business, product, process, and data problems with evidence and falsifiable hypotheses, then explains the root cause clearly | “Investigate the root cause read-only, explain it to a beginner, and ask before fixing it.” |
| [explain-to-master](explain-to-master/) | Builds real understanding through two-layer explanations, reverse-engineered examples, concrete cases, and transfer tests | “Explain it in plain and technical language, then test me with a new case.” |
| [fable-writer](fable-writer/) | Explains an abstract concept through a concise fable and a comprehension check | “Explain sunk cost with a fable.” |
| [first-principles-adversarial-review](first-principles-adversarial-review/) | Reconstructs a problem from first principles and actively searches for counterevidence, omissions, and incorrect sources of truth | “Do not accept my plan at face value. Review the mechanism and counterevidence first.” |
| [kakarot-repurposer](kakarot-repurposer/) | Adapts one source article for Xiaohongshu, Douyin, and Bilibili | “Repurpose this article for multiple platforms.” |
| [human-writing](kakarot-human-writing/) | Writes grounded prose with clear judgment and a natural Chinese rhythm | “Turn these notes into a well-supported article that sounds human.” |
| [kakarot-writer](kakarot-writer/) | Checks sources and AI relevance, then delivers a complete long-form article in Kakarot's personal style | “Write an article in my own style.” |
| [leader](leader/) | Turns a one-line idea into an independently executable task brief for an agent | “Turn this idea into an actionable brief.” |
| [life-designer](life-designer/) | Produces three five-year Odyssey Plans with life-design methods | “I am considering a career change. Help me work through it systematically.” |
| [peer-pr-review](peer-pr-review/) | Adversarially reviews code changes and walks through the real before-and-after path with one concrete case | “I do not know this code. Walk me through one case, then tell me what should change.” |
| [project-aware-coding](project-aware-coding/) | Studies existing project logic, design, and history before implementing the smallest change that fits real consumers | “Implement this using the project's existing patterns without repeating old mistakes.” |
| [review-handoff](review-handoff/) | Creates a Markdown review handoff that can be sent directly to a colleague, with a concrete walkthrough when needed | “Turn my PR into a Markdown handoff and explain the path with one case.” |
| [resume-optimizer](resume-optimizer/) | Writes, improves, or reviews a software engineer's résumé | “Review this résumé as a technical interviewer.” |
| [steelman-before-answer](steelman-before-answer/) | Steelmans both sides in the background, then presents a three-part plain-language trade-off and asks one question only when a meaningful choice exists | “Think one level deeper in the background and explain any real trade-off plainly.” |
| [storage-analyzer](storage-analyzer/) | Scans disk usage read-only and produces a tiered cleanup report | “My computer is running out of space. Show me what is using it.” |
| [system-structure-diagram](system-structure-diagram-skill/) | Generates a system structure diagram from a visual reference and real project modules | “Draw the project structure in the style of this image.” |
| [wechat-publisher](wechat-publisher/) | Separates public copy from delivery notes, validates images and links, then saves an article to WeChat Official Account drafts | “Save this article to my WeChat Official Account drafts.” |

## Installation

Install all skills:

```bash
npx skills add Zhangs-11/zs-skills
```

Install one skill:

```bash
npx skills add Zhangs-11/zs-skills --skill aihot
```

List the names discoverable in this repository:

```bash
npx skills add Zhangs-11/zs-skills --list
```

Restart Claude Code or Codex, or open a new session, after installation so the tool discovers the skills again.

## Requirements and safety boundaries

- [ ] Install Node.js and `npx`; verify them with `node --version && npx --version`.
- [ ] Install `human-writing` with `kakarot-writer`. For real source material or AI key art in two cover sizes, also install `guizang-social-card-skill`.
- [ ] Exporting a PNG with `system-structure-diagram` requires a browser or SVG conversion tool. Generating SVG alone does not require Inkscape.
- [ ] `wechat-publisher` requires Python 3.12+, a WeChat Official Account AppID and AppSecret, and an allowed IP address. It performs a read-only preflight before writing a draft.
- [ ] `storage-analyzer` scans read-only. Every deletion requires separate user confirmation, and the reclaimable-space estimate is approximate.
- [ ] `aihot` and `ai-hot-picker` access AI HOT's public API. They require a network connection but no API key.
- [ ] `dating-chat-coach` provides communication guidance rather than manipulation scripts. Safety takes priority when fraud or in-person meeting risks appear.
- [ ] `peer-pr-review` needs read access to the target PR, Git workspace, or worktree. `review-handoff` needs access to the PR or repository. Neither comments, approves, merges, commits, or pushes by default, and neither presents the current `main` branch as proof of a deployed environment.
- [ ] `project-aware-coding` needs read access to the target repository and project instructions. It studies existing code and history without copying them mechanically, and never commits, pushes, or deploys without current authorization.
- [ ] `clarify-before-action` and `diagnose-and-explain` may investigate read-only on their own. Implementation, repairs, data writes, and other external changes require explicit confirmation after the scope is explained.
- [ ] `steelman-before-answer` does not add a clarification round by default. It asks only when a user choice would materially change the result. To apply it consistently in both Codex and Claude Code, add its background entry point to the global `AGENTS.md` and `CLAUDE.md` respectively.

The remaining prompt-only skills have no additional dependencies. Each directory's README lists more specific inputs, outputs, and limitations.

## Automated repository checks

On every push to `main`, pull request, and manual workflow run, GitHub Actions validates skill frontmatter, directory and skill names, `agents/openai.yaml`, evaluation JSON, local Markdown links, tracked high-confidence credentials, and dangerous credential files.

Run the same checks locally:

```bash
python3 -m pip install -r scripts/requirements-ci.txt
python3 scripts/validate_repo.py
```

The scanner reads only Git-tracked content. It does not execute scripts bundled with individual skills or upload files to a third-party scanning service. Credential findings show only the file and line number, never the suspected secret itself.

## Recommended workflows

A content-production workflow can combine several skills:

```text
ai-hot-picker selects a topic
        ↓
kakarot-writer establishes the author's position and sources, then passes the AI-value gate
        ↓
human-writing produces natural, reliable prose
        ↓
kakarot-writer completes personal review, titles, images, and covers
        ↓
after author edits, compare the real draft and final copy to propose personal preference candidates for confirmation
        ↓
publish the same source article to WeChat, Zhihu, blogs, Juejin, and Bilibili columns
        ↓
kakarot-repurposer optionally adapts it for Xiaohongshu, Douyin, and Bilibili video
        ↓
wechat-publisher saves a WeChat draft only after an explicit publishing request
```

Learning and execution can also work together. If an explanation still feels vague, use `explain-to-master` to build intuition with one concrete case, then solidify understanding through one-question-at-a-time prompting and teach-back. When it is time to execute, use `leader` to turn the goal into an acceptance-ready task brief.

For systematic research into a product, company, person, technology, or industry, use `deep-research` to build a framework around historical turning points and real alternatives, then separate key claims into facts, inferences, and value judgments. Simple fact lookups and today's news do not require the full research workflow.

`steelman-before-answer` is the background review entry point for every new task. It internally strengthens both sides and looks for key variables. Ordinary tasks show only the result. When two fact-checked directions remain viable, require a user choice, and have meaningfully different costs, it presents **My judgment / How the two directions differ / What I need you to confirm** in plain language. Substantive tasks then use `first-principles-adversarial-review` as their reasoning foundation before routing to requirement clarification, diagnosis, review, implementation, or writing skills.

Requirements and incidents follow separate paths:

```text
Preparing a new feature or complex task
        ↓
clarify-before-action investigates and clarifies context, requirements, pain points, scope, and acceptance criteria
        ↓
implementation begins after user confirmation

An issue already exists and the cause is unknown
        ↓
diagnose-and-explain locates and explains the root cause with sources, controls, and falsifiable hypotheses
        ↓
repairs begin after user confirmation
```

Code-review collaboration can combine these skills:

```text
peer-pr-review examines a colleague's PR or local/worktree changes and walks through the before-and-after path with beginner-friendly language and one concrete case
        ↓
review-handoff turns your own PR into a directly shareable Markdown handoff, adding a concrete walkthrough when needed
        ↓
change-meeting-brief compresses the requirement, PR, or review document into a 20–40 second meeting update
```

## Repository structure

Each top-level directory is an independent skill:

```text
<skill-name>/
├── SKILL.md       # Trigger description and execution instructions
├── README.md      # Installation and usage documentation for people
├── scripts/       # Optional deterministic scripts
├── references/    # Optional references loaded on demand
└── assets/        # Optional templates and static resources
```

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `No valid skills found` | Invalid `SKILL.md` frontmatter or an incorrect repository path | Run `npx skills add Zhangs-11/zs-skills --list` and verify that the target name exists |
| A skill does not trigger after installation | The current session has not refreshed the skill list, or the prompt is too vague | Open a new session and retry with a natural-language example from the table |
| Only one skill should be installed | The default command opens multi-select or installs several skills | Add `--skill <name>`, using the exact name shown by `--list` |
| A script reports a missing path | The skill was installed under a different agent's directory | Resolve scripts from the current skill root first; reinstall for the current agent if necessary |
| WeChat publishing fails with `40164` | The current public IP is not on the Official Account allowlist | Add the IP shown in the error to the WeChat Official Account platform, then rerun the preflight and publish |

## License

MIT. See [LICENSE](LICENSE).
