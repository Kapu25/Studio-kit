# content-studio-kit

A content studio kit: agents, skills, memory and an escalation hook for video, social and homeschool work.

@memory/MEMORY.md

## Where things live
- `.claude/agents/` agents (model + effort pinned in each file; `*-xhigh.md` are generated escalation twins). `.claude/skills/` skills. `.claude/hooks/` agent-router + memory-nudge.
- `memory/` rules and decisions, one file each; `memory/MEMORY.md` is the index.
- `channels/` style guides. `workflows/` run orders. `brand/` brand files. `projects/<channel>/<date>-<slug>/` work. These are your own folders.
- Optional: keep a private notes file for owner background; never commit it.

## Model routing (saves tokens)
- Main session = supervisor: brief one agent at a time, check what comes back, report to the owner.
- Opus, high: film and judgement agents (motion-director, motion-designer, video-editor, creative-director, script-director, qa-reviewer).
- Sonnet, high: routine agents (captions, subtitles, file moves, lookups, renders, homeschool).
- Never above xhigh, never other than Opus/Sonnet, unless the owner asks. Never xhigh by default.
- Agent fails: the agent-router hook escalates (Sonnet high -> Sonnet xhigh -> Opus -> main session). Redo only the failed part.

## Never
- Publish, upload, schedule, spend, or use a paid tool without the owner's explicit yes and a cost estimate.
- Call anything final before the owner says the literal word "Approved".
- Use footage without a licence record (sources.json), and never run a video downloader.
- Edit an approved job, or let a skill's rules beat ours.

## Memory
- Read memory/MEMORY.md first; open only the file you need.
- Correction or "save this to memory": new file in memory/ + one line in MEMORY.md, automatically.
