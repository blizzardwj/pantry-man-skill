#!/usr/bin/env python3
"""L1 static validation for pantry-man-skill (zero LLM, deterministic).

Automates the AGENTS.md Verification Checklist. Run from anywhere:

    python3 dev/validate_static.py
    python3 dev/validate_static.py --data /path/to/pantry.json

Exit code: 0 if no FAIL (warnings allowed), 1 if any FAIL.
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "SKILL.md"
REFERENCES = REPO / "references"

FAILS = []
WARNS = []


def fail(msg):
    FAILS.append(msg)
    print(f"  \u274c {msg}")


def warn(msg):
    WARNS.append(msg)
    print(f"  \u26a0\ufe0f  {msg}")


def ok(msg):
    print(f"  \u2705 {msg}")


def read(p):
    return p.read_text(encoding="utf-8")


def check_frontmatter():
    print("\n[1] SKILL.md frontmatter")
    text = read(SKILL)
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        fail("no YAML frontmatter (--- ... ---)")
        return
    fm = m.group(1)
    if not re.search(r"^name:\s*pantry-man\s*$", fm, re.MULTILINE):
        fail("frontmatter missing `name: pantry-man`")
    else:
        ok("name: pantry-man")
    desc = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
    if not desc or not desc.group(1).strip():
        fail("frontmatter missing/empty `description`")
    else:
        ok("description present")


def check_references():
    print("\n[2] reference path integrity")
    text = read(SKILL)
    referenced = set(re.findall(r"references/[\w\-]+\.md", text))
    missing = [r for r in referenced if not (REPO / r).exists()]
    if missing:
        for r in sorted(missing):
            fail(f"SKILL.md references missing file: {r}")
    elif referenced:
        ok(f"{len(referenced)} reference(s) cited in SKILL.md all exist")
    else:
        warn("no references/*.md cited in SKILL.md")

    print("\n[3] orphan references (in references/ but never cited)")
    actual = {f"references/{p.name}" for p in REFERENCES.glob("*.md")}
    orphans = actual - referenced
    if orphans:
        for o in sorted(orphans):
            warn(f"orphan reference (not cited in SKILL.md): {o}")
    else:
        ok("no orphan references")


def check_agent_specific():
    print("\n[4] agent-specific paths / commands")
    files = [SKILL] + sorted(REFERENCES.glob("*.md"))
    hardcode = re.compile(r"~/(hermes|claude|cursor|codex|config)/")
    found = False
    for f in files:
        for i, line in enumerate(read(f).splitlines(), 1):
            if hardcode.search(line):
                found = True
                fail(f"{f.relative_to(REPO)}:{i}: hardcoded agent path -> {line.strip()}")
    if not found:
        ok("no hardcoded agent paths")

    cron = re.compile(r"\bcron add\b")
    for f in files:
        hits = len(cron.findall(read(f)))
        if hits:
            warn(
                f"{f.relative_to(REPO)}: {hits}x `cron add` "
                "(known exception - placeholder, see DECISIONS 2026-08-05)"
            )


def check_schema_coverage(data_path):
    print(f"\n[5] schema field coverage (--data {data_path})")
    import json
    try:
        data = json.loads(Path(data_path).read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"cannot load data file: {e}")
        return
    schema_text = read(REFERENCES / "schema.md")

    keys = set()

    def collect(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                keys.add(k)
                collect(v)
        elif isinstance(obj, list):
            for it in obj:
                collect(it)

    collect(data)
    missing = sorted(k for k in keys if k not in schema_text)
    if missing:
        for k in missing:
            warn(f"key not mentioned in schema.md: {k}")
    else:
        ok(f"all {len(keys)} data keys mentioned in schema.md")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", help="real data file for schema field coverage check")
    args = ap.parse_args()

    print(f"pantry-man-skill static validation\nrepo: {REPO}")
    check_frontmatter()
    check_references()
    check_agent_specific()
    if args.data:
        check_schema_coverage(args.data)

    print("\n" + "=" * 44)
    print(f"FAIL: {len(FAILS)}   WARN: {len(WARNS)}")
    if FAILS:
        print("Result: \u274c FAIL")
        sys.exit(1)
    print("Result: \u2705 PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
