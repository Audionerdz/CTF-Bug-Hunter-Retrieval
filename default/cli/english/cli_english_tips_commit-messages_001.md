---
chunk_id: cli::english::tips::commit-messages::001
domain: cli
chunk_type: guide
category: best-practices
confidence: high
reuse_level: universal
tags: [tips, commit, message, best-practice, english]
---

## Tip: Effective Commit Messages

```bash
# Bad - not descriptive
git commit -m "update"

# Good - clear and specific
git commit -m "fix: Correct typo in README.md"

# Better - with context
git commit -m "feat: Add SQL injection guide with 5 payloads

- Includes bypass techniques
- Real lab examples
- Remediation section"
```
