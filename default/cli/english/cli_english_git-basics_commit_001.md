---
chunk_id: cli::english::git-basics::commit::001
domain: cli
chunk_type: guide
category: git-operations
confidence: high
reuse_level: universal
tags: [git, commit, message, english]
---

## Create a Commit

```bash
# Simple commit
git commit -m "Fix typo in README"

# Commit with detailed message
git commit -m "fix: Update vectorizer instructions

- Added venv activation step
- Clarified dependency installation
- Added troubleshooting section"

# View commit history
git log --oneline -10
```
