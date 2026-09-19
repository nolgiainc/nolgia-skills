#!/usr/bin/env python3
"""Lint the skills in this repo.

Conventions (shared with nolgia-agent's marketplace abilities, NOL-884):
  * every skills/<dir>/SKILL.md opens with YAML frontmatter whose `name`
    equals <dir> and follows the Agent Skills naming rules;
  * `version` is present and equals the repo-wide VERSION file;
  * `description` is at most 1024 characters and carries both a
    "Use when" trigger and a "NOT for" boundary;
  * every `metadata.related_skills` entry names a skill in this repo;
  * the body warns above 600 lines and fails above 2,000;
  * no skill reaches outside its own folder (`../`), so each one installs
    standalone;
  * every plugin manifest carries the same version as VERSION.

Exit 0 when clean (warnings allowed), 1 on any error.
"""

import json
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
WARN_LINES = 600
FAIL_LINES = 2000
DESCRIPTION_MAX = 1024


def frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return yaml.safe_load(text[4:end]), text[end + 5 :]


def main():
    errors, warnings = [], []
    version = (ROOT / "VERSION").read_text().strip()
    skill_dirs = sorted(p.parent for p in (ROOT / "skills").glob("*/SKILL.md"))
    names = {d.name for d in skill_dirs}
    if not skill_dirs:
        errors.append("no skills/*/SKILL.md found")

    for d in skill_dirs:
        path = d / "SKILL.md"
        rel = path.relative_to(ROOT)
        meta, body = frontmatter(path.read_text())
        if not isinstance(meta, dict):
            errors.append(f"{rel}: missing or unparsable YAML frontmatter")
            continue
        name = meta.get("name")
        if name != d.name:
            errors.append(f"{rel}: name {name!r} must equal the directory name {d.name!r}")
        if not isinstance(name, str) or not NAME_RE.match(name) or len(name) > 64:
            errors.append(f"{rel}: name {name!r} breaks the Agent Skills naming rules")
        if str(meta.get("version", "")) != version:
            errors.append(f"{rel}: version {meta.get('version')!r} must equal VERSION {version!r}")
        desc = meta.get("description")
        if not isinstance(desc, str) or not desc.strip():
            errors.append(f"{rel}: description is missing")
        else:
            if len(desc) > DESCRIPTION_MAX:
                errors.append(f"{rel}: description is {len(desc)} chars (max {DESCRIPTION_MAX})")
            if "Use when" not in desc:
                errors.append(f"{rel}: description needs a 'Use when' trigger")
            if "NOT for" not in desc:
                errors.append(f"{rel}: description needs a 'NOT for' boundary")
        related = (meta.get("metadata") or {}).get("related_skills") or []
        for other in related:
            if other not in names:
                errors.append(f"{rel}: related skill {other!r} does not exist in skills/")
        lines = body.count("\n")
        if lines > FAIL_LINES:
            errors.append(f"{rel}: body is {lines} lines (fails above {FAIL_LINES})")
        elif lines > WARN_LINES:
            warnings.append(f"{rel}: body is {lines} lines (warns above {WARN_LINES})")
        for f in d.rglob("*"):
            if f.is_file() and f.suffix in {".md", ".sh", ".py"} and "../" in f.read_text():
                errors.append(f"{f.relative_to(ROOT)}: references a path outside its skill folder (../)")

    manifests = {
        ".claude-plugin/plugin.json": lambda m: m["version"],
        ".claude-plugin/marketplace.json": lambda m: m["plugins"][0]["version"],
        ".cursor-plugin/plugin.json": lambda m: m["version"],
        ".codex-plugin/plugin.json": lambda m: m["version"],
    }
    for rel, get in manifests.items():
        try:
            got = get(json.loads((ROOT / rel).read_text()))
        except Exception as exc:  # noqa: BLE001 - report any manifest problem
            errors.append(f"{rel}: unreadable ({exc})")
            continue
        if got != version:
            errors.append(f"{rel}: version {got!r} must equal VERSION {version!r}")

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"{len(skill_dirs)} skill(s) checked, {len(warnings)} warning(s), {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
