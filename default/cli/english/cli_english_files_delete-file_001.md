---
chunk_id: cli::english::files::delete-file::001
domain: cli
chunk_type: guide
category: file-operations
confidence: high
reuse_level: universal
tags: [git, delete, remove, file, english]
---

## Delete Files from Repository

```bash
# Delete file and stage removal
git rm filename.md

# Delete entire directory
git rm -r directory/

# Commit the deletion
git commit -m "docs: Remove obsolete file"

# Push changes
git push origin main
```
