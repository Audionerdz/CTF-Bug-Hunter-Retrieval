---
chunk_id: cli::english::recovery::undo-before-stage::001
domain: cli
chunk_type: technique
---

## Undo Changes Before Staging

```bash
# See what changed
git status
git diff filename.md

# Option 1: Restore original file
git restore filename.md

# Option 2: Use checkout
git checkout filename.md

# Discard ALL changes
git restore .
```
