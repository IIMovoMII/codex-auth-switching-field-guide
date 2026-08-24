from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "README.md",
    "README.en.md",
    "SKILL.md",
    "SKILL.en.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CONTRIBUTING.en.md",
    "SECURITY.md",
    "SECURITY.en.md",
    "references/discovery.md",
    "references/discovery.en.md",
    "references/architecture.md",
    "references/architecture.en.md",
    "references/config-recovery.md",
    "references/config-recovery.en.md",
    "references/first-use-bootstrap.md",
    "references/first-use-bootstrap.en.md",
    "references/history-compatibility.md",
    "references/history-compatibility.en.md",
    "references/multi-relay-profiles.md",
    "references/multi-relay-profiles.en.md",
    "references/network-diagnostics.md",
    "references/network-diagnostics.en.md",
    "references/safety-and-rollback.md",
    "references/safety-and-rollback.en.md",
    "references/validation.md",
    "references/validation.en.md",
}

CHINESE_PRIMARY = {
    relative
    for relative in REQUIRED
    if relative.endswith(".md")
    and not relative.endswith(".en.md")
    and relative != "LICENSE"
}

TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".txt", ".svg"}

PRIVATE_PATTERNS = {
    "Windows 用户绝对路径": re.compile(
        r"(?i)\b[a-z]:\\users\\(?!<|%)[^\\\s]+"
    ),
    "OpenAI 样式密钥": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    "GitHub 令牌": re.compile(r"\b(?:ghp_|github_pat_)[A-Za-z0-9_]{16,}\b"),
    "微信账号标识": re.compile(r"\bwxid_[A-Za-z0-9_]+\b", re.IGNORECASE),
    "已填写的应用密钥": re.compile(
        r"(?i)\bapp[_ -]?secret\b\s*[:=]\s*[\"']?(?!<)[A-Za-z0-9_-]{8,}"
    ),
}

LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def iter_text_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix.lower() in TEXT_SUFFIXES
    )


def validate_required(errors: list[str]) -> None:
    for relative in sorted(REQUIRED):
        if not (ROOT / relative).is_file():
            errors.append(f"缺少必要文件：{relative}")


def validate_skill(errors: list[str]) -> None:
    for relative in ("SKILL.md", "SKILL.en.md"):
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            errors.append(f"{relative} 必须以 YAML 前置信息开始")
            continue
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not match:
            errors.append(f"{relative} 的 YAML 前置信息没有闭合")
            continue
        keys = {
            line.split(":", 1)[0].strip()
            for line in match.group(1).splitlines()
            if ":" in line
        }
        if keys != {"name", "description"}:
            errors.append(f"{relative} 的 YAML 前置信息只能包含 name 和 description")


def validate_chinese_primary(errors: list[str]) -> None:
    for relative in sorted(CHINESE_PRIMARY):
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        cjk_count = len(re.findall(r"[\u3400-\u9fff]", text))
        minimum = 50 if relative in {"README.md", "SKILL.md"} or relative.startswith("references/") else 20
        if cjk_count < minimum:
            errors.append(f"默认中文文档的中文内容不足：{relative}")


def normalize_link(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if " " in target:
        target = target.split(" ", 1)[0]
    return target.split("#", 1)[0]


def validate_links(path: Path, text: str, errors: list[str]) -> None:
    for raw in LINK_PATTERN.findall(text):
        target = normalize_link(raw)
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        if target.startswith("/"):
            errors.append(f"{path.relative_to(ROOT)}：不允许仓库内绝对链接 {target}")
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)}：链接超出仓库范围：{target}")
            continue
        if not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)}：链接目标不存在：{target}")


def validate_privacy(path: Path, text: str, errors: list[str]) -> None:
    relative = path.relative_to(ROOT)
    for label, pattern in PRIVATE_PATTERNS.items():
        if pattern.search(text):
            errors.append(f"{relative}：可能包含{label}")


def main() -> int:
    errors: list[str] = []
    validate_required(errors)
    validate_skill(errors)
    validate_chinese_primary(errors)

    for path in iter_text_files():
        text = path.read_text(encoding="utf-8")
        validate_privacy(path, text, errors)
        if path.suffix.lower() == ".md":
            validate_links(path, text, errors)

    if errors:
        print("经验包校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"经验包校验通过：{ROOT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
