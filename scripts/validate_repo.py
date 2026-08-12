#!/usr/bin/env python3
"""Validate the structure and high-confidence safety properties of zs-skills."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

import yaml


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
ALLOWED_DIRECTORY_ALIASES = {
    "kakarot-human-writing": "human-writing",
    "system-structure-diagram-skill": "system-structure-diagram",
}
IGNORED_DIRECTORIES = {".git", ".venv", "node_modules", "__pycache__"}
ENV_EXAMPLE_SUFFIXES = (".example", ".sample", ".template")
SENSITIVE_FILENAMES = {
    ".env",
    "credentials.json",
    "service-account.json",
    "id_rsa",
    "id_dsa",
    "id_ed25519",
}
SENSITIVE_SUFFIXES = {".p12", ".pfx", ".jks", ".keystore"}
SECRET_PATTERNS = {
    "private key": re.compile("-----" + r"BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(?:github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,})\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    "OpenAI-style secret": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
}
PRIVATE_IDENTITY_PATTERNS = {
    "真实中文姓名": re.compile("张" + "硕"),
    "真实姓名拼音": re.compile(r"(?i)\bzhang\s*shuo\b"),
}


@dataclass(frozen=True)
class Finding:
    path: str
    message: str
    line: int | None = None

    def render(self) -> str:
        location = f"{self.path}:{self.line}" if self.line else self.path
        return f"{location}: {self.message}"


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def tracked_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if result.returncode == 0:
        return [root / item.decode() for item in result.stdout.split(b"\0") if item]
    return [
        path
        for path in root.rglob("*")
        if path.is_file() and not any(part in IGNORED_DIRECTORIES for part in path.parts)
    ]


def load_frontmatter(path: Path) -> tuple[dict, list[Finding]]:
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return {}, [Finding(str(path), f"无法读取 UTF-8 文本：{exc}")]
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, [Finding(str(path), "缺少以 --- 开始的 YAML frontmatter", 1)]
    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return {}, [Finding(str(path), "YAML frontmatter 没有结束分隔符")]
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as exc:
        return {}, [Finding(str(path), f"YAML 无法解析：{exc}")]
    if not isinstance(data, dict):
        findings.append(Finding(str(path), "YAML frontmatter 必须是对象"))
        return {}, findings
    return data, findings


def validate_skills(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    seen_names: dict[str, Path] = {}
    skill_files = sorted(path for path in root.glob("*/SKILL.md") if path.is_file())
    if not skill_files:
        return [Finding(".", "没有发现任何一级 Skill 目录")]

    for skill_file in skill_files:
        rel = relative(skill_file, root)
        data, parse_findings = load_frontmatter(skill_file)
        findings.extend(Finding(rel, item.message, item.line) for item in parse_findings)
        if not data:
            continue
        name = data.get("name")
        description = data.get("description")
        if not isinstance(name, str) or not name.strip():
            findings.append(Finding(rel, "frontmatter.name 必须是非空字符串"))
            continue
        if not NAME_RE.fullmatch(name):
            findings.append(Finding(rel, f"Skill 名称不符合小写连字符格式：{name}"))
        if not isinstance(description, str) or not description.strip():
            findings.append(Finding(rel, "frontmatter.description 必须是非空字符串"))
        previous = seen_names.get(name)
        if previous:
            findings.append(Finding(rel, f"Skill 名称与 {relative(previous, root)} 重复：{name}"))
        else:
            seen_names[name] = skill_file

        directory_name = skill_file.parent.name
        expected_name = ALLOWED_DIRECTORY_ALIASES.get(directory_name, directory_name)
        if name != expected_name:
            findings.append(
                Finding(rel, f"目录名 {directory_name} 与 Skill 名称 {name} 不一致；若为兼容别名需显式加入白名单")
            )

        openai_yaml = skill_file.parent / "agents" / "openai.yaml"
        if openai_yaml.exists():
            try:
                interface_data = yaml.safe_load(openai_yaml.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, yaml.YAMLError) as exc:
                findings.append(Finding(relative(openai_yaml, root), f"agents/openai.yaml 无法解析：{exc}"))
                continue
            interface = interface_data.get("interface") if isinstance(interface_data, dict) else None
            prompt = interface.get("default_prompt") if isinstance(interface, dict) else None
            if not isinstance(prompt, str) or f"${name}" not in prompt:
                findings.append(
                    Finding(relative(openai_yaml, root), f"interface.default_prompt 必须显式包含 ${name}")
                )
    return findings


def validate_evals(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for eval_file in sorted(root.glob("*/evals/evals.json")):
        rel = relative(eval_file, root)
        try:
            data = json.loads(eval_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            findings.append(Finding(rel, f"评测 JSON 无法解析：{exc}"))
            continue
        skill_file = eval_file.parents[1] / "SKILL.md"
        frontmatter, _ = load_frontmatter(skill_file)
        if not isinstance(data, dict):
            findings.append(Finding(rel, "评测文件根节点必须是对象"))
            continue
        if data.get("skill_name") != frontmatter.get("name"):
            findings.append(Finding(rel, "skill_name 必须与同目录 SKILL.md 的 name 一致"))
        evals = data.get("evals")
        if not isinstance(evals, list) or not evals:
            findings.append(Finding(rel, "evals 必须是非空数组"))
            continue
        seen_ids: set[object] = set()
        for index, case in enumerate(evals, start=1):
            label = f"第 {index} 个评测"
            if not isinstance(case, dict):
                findings.append(Finding(rel, f"{label}必须是对象"))
                continue
            case_id = case.get("id")
            if case_id in seen_ids:
                findings.append(Finding(rel, f"评测 id 重复：{case_id}"))
            seen_ids.add(case_id)
            for field in ("prompt", "expected_output"):
                if not isinstance(case.get(field), str) or not case[field].strip():
                    findings.append(Finding(rel, f"{label}缺少非空 {field}"))
            if "files" in case and not isinstance(case["files"], list):
                findings.append(Finding(rel, f"{label}的 files 必须是数组"))
            if "expectations" in case and (
                not isinstance(case["expectations"], list)
                or not all(isinstance(item, str) and item.strip() for item in case["expectations"])
            ):
                findings.append(Finding(rel, f"{label}的 expectations 必须是非空字符串数组"))
    return findings


def normalized_link_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = target.split(maxsplit=1)[0]
    target = unquote(target).split("#", 1)[0]
    if not target or target.lower() in {"url", "<url>"}:
        return None
    if target.startswith(("http://", "https://", "mailto:", "tel:", "data:")):
        return None
    if any(marker in target for marker in ("<", ">", "{", "}", "$")):
        return None
    return target


def validate_markdown_links(root: Path, files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in files:
        if path.suffix.lower() != ".md" or not path.exists():
            continue
        rel = relative(path, root)
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            findings.append(Finding(rel, f"Markdown 无法读取：{exc}"))
            continue
        in_fence = False
        fence = ""
        for line_number, line in enumerate(lines, start=1):
            stripped = line.lstrip()
            if stripped.startswith(("```", "~~~")):
                marker = stripped[:3]
                if not in_fence:
                    in_fence, fence = True, marker
                elif marker == fence:
                    in_fence = False
                continue
            if in_fence:
                continue
            for match in MARKDOWN_LINK_RE.finditer(line):
                target = normalized_link_target(match.group(1))
                if target is None:
                    continue
                candidate = (path.parent / target).resolve()
                try:
                    candidate.relative_to(root.resolve())
                except ValueError:
                    findings.append(Finding(rel, f"本地链接越过仓库边界：{target}", line_number))
                    continue
                if not candidate.exists():
                    findings.append(Finding(rel, f"本地链接目标不存在：{target}", line_number))
    return findings


def is_env_example(path: Path) -> bool:
    return path.name.endswith(ENV_EXAMPLE_SUFFIXES) or ".env.example" in path.name


def validate_secrets(root: Path, files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in files:
        if not path.exists() or not path.is_file():
            continue
        rel = relative(path, root)
        lowered = path.name.lower()
        is_environment_file = (
            lowered == ".env"
            or lowered.startswith(".env.")
            or lowered.endswith(".env")
            or ".env." in lowered
        )
        is_sensitive_name = lowered in SENSITIVE_FILENAMES or is_environment_file
        if (is_sensitive_name and not is_env_example(path)) or path.suffix.lower() in SENSITIVE_SUFFIXES:
            findings.append(Finding(rel, "高风险凭据文件不应被 Git 跟踪"))
        try:
            if path.stat().st_size > 2_000_000:
                continue
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(line):
                    findings.append(Finding(rel, f"发现疑似真实 {label}；只报告位置，不回显内容", line_number))
    return findings


def validate_public_identity(root: Path, files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in files:
        if not path.exists() or not path.is_file():
            continue
        rel = relative(path, root)
        try:
            if path.stat().st_size > 2_000_000:
                continue
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for label, pattern in PRIVATE_IDENTITY_PATTERNS.items():
                if pattern.search(line):
                    findings.append(
                        Finding(rel, f"公开文件含{label}；统一使用 Kakarot，不回显命中内容", line_number)
                    )
    return findings


def run(root: Path) -> list[Finding]:
    files = tracked_files(root)
    findings: list[Finding] = []
    findings.extend(validate_skills(root))
    findings.extend(validate_evals(root))
    findings.extend(validate_markdown_links(root, files))
    findings.extend(validate_secrets(root, files))
    findings.extend(validate_public_identity(root, files))
    return sorted(findings, key=lambda item: (item.path, item.line or 0, item.message))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    findings = run(root)
    if findings:
        print(f"仓库质检失败：{len(findings)} 个问题", file=sys.stderr)
        for finding in findings:
            print(f"- {finding.render()}", file=sys.stderr)
        return 1
    skill_count = len(list(root.glob("*/SKILL.md")))
    eval_count = len(list(root.glob("*/evals/evals.json")))
    print(f"仓库质检通过：{skill_count} 个 Skills，{eval_count} 份评测文件；本地链接与高置信凭据扫描通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
