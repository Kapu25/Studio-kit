---
name: memory-system
label: How memory works (read first, save on correction)
date: 2026-11-13
source: owner
---
- Every session reads memory/MEMORY.md first (CLAUDE.md imports it), then opens only the memory file it needs.
- When the owner corrects something or says "save this to memory": write ONE new file memory/<short-kebab-name>.md
  (frontmatter: name, label, date, source; then the rule, the reason, any exception) and add ONE line to MEMORY.md:
  `- [Label](file.md): one-line summary`. Do it automatically, without being asked again.
- If it changes an older rule, update that file (note what changed) instead of adding a duplicate.
- The memory-nudge hook reminds the session when a message looks like a correction.
- Rebuild the index any time with `python3 tools/memory_index.py memory`.
