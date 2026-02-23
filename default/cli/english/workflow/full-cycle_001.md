---
chunk_id: cli::english::workflow::full-cycle::001
domain: cli
chunk_type: technique
---

## Complete Cycle: Changes → Commit → Push

```bash
# 1. Start day by getting latest
git pull

# 2. Make changes to files
nano docs/my-guide.md

# 3. Check what changed
git status

# 4. Stage all changes
git add .

# 5. Commit with descriptive message
git commit -m "feat: Add new exploitation guide"

# 6. Push to GitHub
git push origin main

# 7. Verify it pushed
git log --oneline -3
```
