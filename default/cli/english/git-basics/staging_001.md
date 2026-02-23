---
chunk_id: cli::english::git-basics::staging::001
domain: cli
chunk_type: technique
---

## Stage Files for Commit

```bash
# Stage one file
git add filename.md

# Stage all changes
git add .

# Stage all except one
git add . && git reset exclude-file.md

# Unstage a file
git reset filename.md

# Unstage all files
git reset
```
