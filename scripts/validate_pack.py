from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "README.md",
    "README.zh-CN.md",
    "SKILL.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "references/discovery.md",
    "references/architecture.md",
    "references/history-compatibility.md",
    "references/network-diagnostics.md",
    "references/safety-and-rollback.md",
    "references/validation.md",
}

TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".txt", ".svg"}

PRIVATE_PATTERNS = {
    "absolute Windows user path": re.compile(
        r"(?i)\b[a-z]:\\users\\(?!<|%)[^\\\s]+"
    ),
    "OpenAI-style secret": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    "GitHub token": re.compile(r"\b(?:ghp_|github_pat_)[A-Za-z0-9_]{16,}\b"),
    "WeChat identifier": re.compile(r"\bwxid_[A-Za-z0-9_]+\b", re.IGNORECASE),
    "assigned app secret": re.compile(
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
            errors.append(f"missing required file: {relative}")


def validate_skill(errors: list[str]) -> None:
    path = ROOT / "SKILL.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append("SKILL.md must start with YAML frontmatter")
        return
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        errors.append("SKILL.md frontmatter is not closed")
        return
    keys = {
        line.split(":", 1)[0].strip()
        for line in match.group(1).splitlines()
        if ":" in line
    }
    if keys != {"name", "description"}:
        errors.append("SKILL.md frontmatter must contain only name and description")


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
            errors.append(f"{path.relative_to(ROOT)}: absolute link {target}")
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)}: link leaves repository: {target}")
            continue
        if not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)}: broken link: {target}")


def validate_privacy(path: Path, text: str, errors: list[str]) -> None:
    relative = path.relative_to(ROOT)
    for label, pattern in PRIVATE_PATTERNS.items():
        if pattern.search(text):
            errors.append(f"{relative}: possible {label}")


def main() -> int:
    errors: list[str] = []
    validate_required(errors)
    validate_skill(errors)

    for path in iter_text_files():
        text = path.read_text(encoding="utf-8")
        validate_privacy(path, text, errors)
        if path.suffix.lower() == ".md":
            validate_links(path, text, errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validation passed for {ROOT.name}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
