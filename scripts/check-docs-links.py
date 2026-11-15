#!/usr/bin/env python3
"""Verify that every relative Markdown link in README.md, CHANGELOG.md and docs/ resolves
(file exists, and #anchors exist in the target file). Exit 1 on any broken link."""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
files = [ROOT / "README.md", ROOT / "CHANGELOG.md"] + sorted((ROOT / "docs").rglob("*.md"))

def anchors(path):
    out = set()
    in_code = False
    for line in path.read_text().splitlines():
        if line.startswith("```"):
            in_code = not in_code
        m = None if in_code else re.match(r"^#{1,6}\s+(.*)$", line)
        if m:
            t = re.sub(r"[`*]", "", m.group(1)).strip().lower()
            t = re.sub(r"[^\w\- ]", "", t).replace(" ", "-")
            out.add(t)
    return out

bad = 0
for f in files:
    in_code = False
    for n, line in enumerate(f.read_text().splitlines(), 1):
        if line.startswith("```"):
            in_code = not in_code
        if in_code:
            continue
        for m in re.finditer(r"\[[^\]]*\]\(([^)\s]+)\)", re.sub(r"`[^`]*`", "", line)):
            target = m.group(1)
            if re.match(r"^(https?:|mailto:)", target):
                continue
            path, _, frag = target.partition("#")
            dest = f if not path else (f.parent / path).resolve()
            if not dest.exists():
                print(f"{f.relative_to(ROOT)}:{n}: missing file {target}"); bad += 1; continue
            if frag and dest.suffix == ".md" and frag.lower() not in anchors(dest):
                print(f"{f.relative_to(ROOT)}:{n}: missing anchor {target}"); bad += 1
print("broken links:", bad)
sys.exit(1 if bad else 0)
