---
chunk_id: cli::english::recovery::undo-commit::001
domain: cli
chunk_type: guide
category: recovery
confidence: high
reuse_level: universal
tags: [git, revert, reset, undo-commit, english]
---

## Undo a Commit (Before Pushing)

```bash
# Option 1: Keep changes, undo commit only
git reset --soft HEAD~1

# Option 2: Discard everything (PERMANENT)
git reset --hard HEAD~1

# Check history
git log --oneline -5
```
