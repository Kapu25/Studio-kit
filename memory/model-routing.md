---
name: model-routing
label: Model routing (saves tokens)
date: 2026-11-13
source: owner
---
- The main session is the supervisor: it briefs agents, checks results, reports to the owner.
- Every agent file pins `model:` AND `effort:` in its frontmatter (tools/pin_agents.py does it; `--verify` checks it).
- Opus, effort high: film and judgement agents: motion-director, motion-designer, video-editor, creative-director, script-director, qa-reviewer, and any agent that edits or reviews a film.
- Sonnet, effort high: routine agents: captions, subtitle-agent, file moves, lookups, renders, homeschool agents, everything else.
- Never above xhigh, never a model other than Opus or Sonnet, unless the owner asks. Match effort to the task; never xhigh by default.
- One agent at a time unless the owner asks for speed (then set KIT_PARALLEL=1).
- Never fork the whole conversation into a helper. Give a short brief instead.
- When an agent fails: [agent-escalation](agent-escalation.md).
