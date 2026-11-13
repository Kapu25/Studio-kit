---
name: approve-renames-three-files
label: Approve renames only the 3 build files
date: 2026-11-13
source: owner
---
- The approve step renames ONLY the three build files in out/: the master `<job>_DRAFT-NOT-APPROVED.mp4`, its `.srt`, and the burned-caption preview.
- Any other file in out/ (previews, test renders) keeps its name.
- The approve step refuses if the master is missing and lists any DRAFT file it leaves alone.
