---
name: agent-escalation
label: Agent fails -> automatic escalation
date: 2026-11-13
source: owner
---
- Hook: .claude/hooks/agent-router.py (PreToolUse + PostToolUse + PostToolUseFailure on the Agent tool).
- Every agent brief gets a closing line request: `STATUS: DONE` or `STATUS: FAILED: <part>`.
- Sonnet agent: 1st Sonnet high -> 2nd Sonnet xhigh (twin file `<name>-xhigh`) -> 3rd Opus -> 4th the main session does it.
- Opus agent: 1st Opus high -> 2nd Opus xhigh (twin) -> 3rd the main session does it.
- Each retry gets ONLY the failed part. Never redo the whole job.
- Paid tools are never retried automatically (see [paid-actions](paid-actions.md)).
- State + log: .claude/state/agent-router.json / .log. A success resets the agent.
