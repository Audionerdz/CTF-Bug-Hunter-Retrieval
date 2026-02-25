---
chunk_id: cli::english::tips::commit-often::001
domain: cli
chunk_type: technique
---

## Tip: Commit Frequently

```bash
# Commit small changes regularly
git add section-1.md
git commit -m "docs: Complete section 1"

git add section-2.md
git commit -m "docs: Complete section 2"

# Push all at end
git push origin main

# Check history
git log --oneline -5
```
