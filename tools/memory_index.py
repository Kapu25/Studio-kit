#!/usr/bin/env python3
"""Rebuild memory/MEMORY.md: one line per memory file (label + link + first rule line). Usage: python3 tools/memory_index.py <memory_dir>"""
import re, sys
from pathlib import Path

GROUPS = [
    ("How I work", ["assistant-role", "memory-system", "main-session-workflow", "model-routing", "agent-escalation", "usage-log", "project-folders"]),
    ("Approval and money", ["approval-literal-approved", "approve-renames-three-files", "approval-gates", "paid-actions", "approved-jobs-frozen"]),
    ("Video style and pacing", ["house-style-tech-videos", "pacing-short-cards", "captions-format", "video-engine-rules", "brand-lock"]),
    ("Footage, facts, voice", ["footage-licensing", "facts-and-sources", "verified-figures", "press-photos-credit", "narration-voice", "flow-clips", "burmese-copy"]),
    ("Channels and departments", ["channels", "homeschool"]),
]
d = Path(sys.argv[1])
files = {p.stem: p for p in d.glob("*.md") if p.name != "MEMORY.md"}
def entry(p):
    t = p.read_text(encoding="utf-8")
    label = re.search(r"^label:\s*(.+)$", t, re.M)
    body = re.split(r"\n---\n", t, maxsplit=1)[-1].strip().splitlines()
    first = next((re.sub(r"^(- |\d+\. )", "", l.strip()) for l in body if l.strip()), "")
    first = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", first)
    first = first if len(first) <= 100 else first[:100].rsplit(" ", 1)[0] + "…"
    return f"- [{label.group(1).strip() if label else p.stem}]({p.name}): {first}"
out = ["# MEMORY index", "",
       "Read this first every session, then open only the file you need. One line per memory file.",
       "New correction or \"save this to memory\": add a file + one line here (see memory-system.md). Rebuild: `python3 tools/memory_index.py memory`.", ""]
used = set()
for title, names in GROUPS:
    rows = [entry(files[n]) for n in names if n in files]
    used |= {n for n in names if n in files}
    if rows:
        out += [f"## {title}"] + rows + [""]
rest = sorted(set(files) - used)
if rest:
    out += ["## Other"] + [entry(files[n]) for n in rest] + [""]
(d / "MEMORY.md").write_text("\n".join(out), encoding="utf-8")
print(f"MEMORY.md: {len(files)} memory files indexed")
