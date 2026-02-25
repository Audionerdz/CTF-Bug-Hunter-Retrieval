---
chunk_id: cli::english::troubleshooting::cannot-push::001
domain: cli
chunk_type: technique
---

## Troubleshooting: Cannot Push to GitHub

```bash
# Check remote connection
git remote -v

# Try pulling first
git pull origin main

# Then try pushing
git push origin main

# If still fails, check branch
git branch -v
```
