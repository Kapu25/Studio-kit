#!/usr/bin/env python3
"""memory-nudge (escalation system): when the owner corrects something or says "save this to memory",
remind the session to save it as a memory file + one index line. Runs on UserPromptSubmit."""
import json, re, sys

SAVE = re.compile(r"\b(save (this|that|it) (to|in) memory|remember (this|that)|add (this|that) to memory|from now on|always |never |rule:|correction)\b", re.I)
CORRECT = re.compile(r"(^|\b)(wrong|not right|that's not|that is not|no,|don't|do not|stop doing|instead of|too long|too short)\b", re.I)

ev = json.load(sys.stdin)
p = ev.get("prompt", "")
if SAVE.search(p) or CORRECT.search(p):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": (
        "[memory-nudge] This message may contain a correction or a rule from the owner. If it does: "
        "1) write it as ONE new file memory/<short-kebab-name>.md (frontmatter: name, label, date, source; then the rule in a few lines, "
        "with the reason and any exception she gave); 2) add ONE line to memory/MEMORY.md: "
        "`- [Label](file.md): one-line summary`; 3) if it replaces an older memory, update that file instead and say what changed. "
        "Do it without being asked again. If the message is not a correction or rule, ignore this.")}}))
