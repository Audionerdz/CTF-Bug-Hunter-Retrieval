---
chunk_id: cli::english::recovery::revert-pushed::001
domain: cli
chunk_type: guide
category: recovery
confidence: high
reuse_level: universal
tags: [git, revert, pushed, github, english]
---

## Undo Changes Already Pushed to GitHub

```bash
# See commit to undo
git log --oneline -5

# Create new commit that reverts it
git revert commit-hash

# Push the revert
git push origin main
```
