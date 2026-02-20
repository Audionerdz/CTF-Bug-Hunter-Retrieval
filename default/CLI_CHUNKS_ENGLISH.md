---
chunk_id: cli::english::setup::configure-git::001
domain: cli
chunk_type: guide
category: git-setup
confidence: high
reuse_level: universal
tags: [setup, git, configuration, english]
---

## Configure Git for the First Time

```bash
# Set your username
git config user.name "Your Name"

# Set your email
git config user.email "your@email.com"

# Verify configuration
git config --list
```

---
chunk_id: cli::english::git-basics::check-status::001
domain: cli
chunk_type: guide
category: git-operations
confidence: high
reuse_level: universal
tags: [git, status, check, english]
---

## Check Git Status

```bash
# See overall status
git status

# See detailed changes
git diff

# See staged changes
git diff --staged

# See changes in one file
git diff filename.md
```

---
chunk_id: cli::english::git-basics::staging::001
domain: cli
chunk_type: guide
category: git-operations
confidence: high
reuse_level: universal
tags: [git, staging, add, english]
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

---
chunk_id: cli::english::recovery::undo-before-stage::001
domain: cli
chunk_type: guide
category: recovery
confidence: high
reuse_level: universal
tags: [git, undo, recovery, english]
---

## Undo Changes Before Staging

```bash
# See what changed
git status
git diff filename.md

# Option 1: Restore original file
git restore filename.md

# Option 2: Use checkout
git checkout filename.md

# Discard ALL changes
git restore .
```

---
chunk_id: cli::english::recovery::undo-staged::001
domain: cli
chunk_type: guide
category: recovery
confidence: high
reuse_level: universal
tags: [git, unstage, reset, english]
---

## Undo Staging (Prepared Changes)

```bash
# Unstage one file
git reset filename.md

# Unstage all files
git reset

# Check status
git status
```

---
chunk_id: cli::english::recovery::undo-commit::001
domain: cli
chunk_type: guide
category: recovery
confidence: high
reuse_level: universal
tags: [git, revert, reset, undo-commit, english]
---

## Undo a Commit (Before Pushing)

```bash
# Option 1: Keep changes, undo commit only
git reset --soft HEAD~1

# Option 2: Discard everything (PERMANENT)
git reset --hard HEAD~1

# Check history
git log --oneline -5
```

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

---
chunk_id: cli::english::files::copy-directory::001
domain: cli
chunk_type: guide
category: file-operations
confidence: high
reuse_level: universal
tags: [files, directory, copy, english]
---

## Copy Directories to Repository

```bash
# Copy entire directory
cp -r /path/to/source /home/kali/Desktop/RAG/dest

# Copy files from directory
cp -r /path/to/source/* /home/kali/Desktop/RAG/dest/

# Create new directory in repo
mkdir -p /home/kali/Desktop/RAG/new-directory
```

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

---
chunk_id: cli::english::github::push::001
domain: cli
chunk_type: guide
category: github
confidence: high
reuse_level: universal
tags: [git, push, github, upload, english]
---

## Push Changes to GitHub

```bash
# After committing, push to main
git push origin main

# Push and verify
git push origin main && git status

# If branch doesn't exist yet
git push -u origin main
```

---
chunk_id: cli::english::github::pull::001
domain: cli
chunk_type: guide
category: github
confidence: high
reuse_level: universal
tags: [git, pull, fetch, download, english]
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

---
chunk_id: cli::english::vectorization::single-file::001
domain: cli
chunk_type: guide
category: vectorization
confidence: high
reuse_level: universal
tags: [vectorization, file, single, english]
---

## Vectorize a Single File

```bash
# From repo root
cd /home/kali/Desktop/RAG

# Vectorize ONE file
python3 src/vectorize_canonical_openai.py ./docs/my-guide.md

# Check result
echo "Vectorization complete!"
```

---
chunk_id: cli::english::vectorization::directory::001
domain: cli
chunk_type: guide
category: vectorization
confidence: high
reuse_level: universal
tags: [vectorization, directory, batch, english]
---

## Vectorize an Entire Directory

```bash
# Vectorize all files in docs/
python3 src/vectorize_canonical_openai.py ./docs/

# Vectorize entire repo
python3 src/vectorize_canonical_openai.py .

# Output will show chunks created
```

---
chunk_id: cli::english::query::how-to-query::001
domain: cli
chunk_type: guide
category: search
confidence: high
reuse_level: universal
tags: [query, search, semantic, english]
---

## How to Query Your Knowledge Base

```bash
# Question in English
python3 src/query_canonical_openai.py "how to revert a commit"

# Question in Spanish
python3 src/query_canonical_openai.py "cómo subir a github"

# General query
python3 src/query_canonical_openai.py "git workflow"
```

---
chunk_id: cli::english::workflow::full-cycle::001
domain: cli
chunk_type: guide
category: workflow
confidence: high
reuse_level: universal
tags: [workflow, cycle, complete, english]
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

---
chunk_id: cli::english::troubleshooting::cannot-push::001
domain: cli
chunk_type: guide
category: troubleshooting
confidence: high
reuse_level: universal
tags: [troubleshooting, push, error, english]
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

---
chunk_id: cli::english::tips::commit-often::001
domain: cli
chunk_type: guide
category: best-practices
confidence: high
reuse_level: universal
tags: [tips, workflow, commit-frequency, english]
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

---
chunk_id: cli::english::reference::quick-commands::001
domain: cli
chunk_type: reference
category: quick-ref
confidence: high
reuse_level: universal
tags: [reference, quick, commands, english]
---

## Quick Reference: Main Commands

```bash
# Check status
git status

# See changes
git diff

# Stage everything
git add .

# Commit
git commit -m "message"

# Push
git push origin main

# Pull
git pull origin main

# View history
git log --oneline -10

# Undo changes
git restore .

# Revert commit
git revert commit-hash
```

