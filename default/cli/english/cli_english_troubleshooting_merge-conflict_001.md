---
chunk_id: cli::english::troubleshooting::merge-conflict::001
domain: cli
chunk_type: guide
category: troubleshooting
confidence: high
reuse_level: universal
tags: [troubleshooting, merge, conflict, english]
---

## Troubleshooting: Merge Conflict

```bash
# When git pull fails
git pull origin main

# Open conflicted file
nano conflicted-file.md

# Look for these markers:
# <<<<<<< HEAD (your changes)
# ======= (divider)
# >>>>>>> origin/main (their changes)

# Edit to keep correct version, remove markers

# Stage and commit
git add conflicted-file.md
git commit -m "fix: Resolve merge conflict"

# Push
git push origin main
```
