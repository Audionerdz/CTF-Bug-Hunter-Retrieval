---
chunk_id: cli::english::github::pull::001
domain: cli
chunk_type: technique
---

## Download Changes from GitHub

```bash
# Get latest without merging
git fetch origin

# See what changed
git log HEAD..origin/main --oneline

# Download and merge
git pull origin main

# Or all in one
git pull
```
