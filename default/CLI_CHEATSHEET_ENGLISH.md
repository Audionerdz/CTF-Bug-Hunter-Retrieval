---
chunk_id: cli::english-guide::setup::001
domain: cli
chunk_type: guide
category: git-and-cli
confidence: high
reuse_level: universal
tags: [cli, git, setup, english, cheatsheet, beginners]
source_file: CLI_CHEATSHEET.md
---

# Absolute Beginner Setup

## First Time Setup (Copy-Paste Ready)

```bash
# 1. Navigate to your repo
cd /home/kali/Desktop/RAG

# 2. Check if git is initialized (should be ✅)
git status

# 3. Configure git (first time only - use your info)
git config user.name "Your Name"
git config user.email "your@email.com"

# 4. Check your configuration
git config --list

# 5. Install Python dependencies
python3 -m pip install -r config/requirements.txt
```

## Verify You're Ready

```bash
# Should show: On branch main, nothing to commit
git status

# Should show your commits
git log --oneline -5
```

---
chunk_id: cli::english-guide::git-basics::001
domain: cli
chunk_type: guide
category: git-and-cli
confidence: high
reuse_level: universal
tags: [cli, git, basics, english, states, workflow]
source_file: CLI_CHEATSHEET.md
---

# Git Basics (Track Changes)

## Understanding Git States

```
WORKING DIR → STAGING AREA → LOCAL REPO → GITHUB
   (files)      (git add)    (git commit)  (git push)
```

## Check What Changed

```bash
# See all modified files
git status

# See detailed changes in files
git diff

# See changes you already staged
git diff --staged

# See changes in ONE file
git diff filename.md
```

## Stage Files for Commit

```bash
# Stage ONE file
git add filename.md

# Stage ALL modified files
git add .

# Stage all files EXCEPT one
git add . && git reset filename.md

# Unstage a file (remove from staging)
git reset filename.md

# Check what you staged
git status
```

---
chunk_id: cli::english-guide::commit-messages::001
domain: cli
chunk_type: guide
category: git-and-cli
confidence: high
reuse_level: universal
tags: [cli, git, commits, messages, english]
source_file: CLI_CHEATSHEET.md
---

# Commit (Save Locally)

## Simple commit
```bash
git commit -m "Fixed typo in README"
```

## Better commit (with details)
```bash
git commit -m "Fix: Update vectorizer instructions for Python 3.10
- Added virtual environment activation steps
- Clarified dependency installation
- Added troubleshooting section"
```

## Commit everything in one go
```bash
git add . && git commit -m "feat: Add new CTF guide for SQL injection"
```

## Check your commits
```bash
git log --oneline -10
```

### Commit Message Format (Pro Tips)

- **Fix**: Brief description
- **Feat**: New feature added
- **Docs**: Documentation updates
- **Refactor**: Code restructuring
- **Test**: Test additions

---
chunk_id: cli::english-guide::undo-mistakes::001
domain: cli
chunk_type: guide
category: git-recovery
confidence: high
reuse_level: universal
tags: [cli, git, undo, revert, recovery, english]
source_file: CLI_CHEATSHEET.md
---

# Reverting & Fixing Mistakes

## "Oops, I Didn't Mean That" - Recovery Guide

### I Edited a File But Haven't Staged It

```bash
# See what changed
git status
git diff filename.md

# Option A: Keep changes but unstage
git reset filename.md

# Option B: Discard changes completely (⚠️ PERMANENT)
git restore filename.md
# OR
git checkout filename.md
```

### I Staged Files But Want to Unstage

```bash
# Unstage ONE file
git reset filename.md

# Unstage ALL files
git reset

# Verify
git status
```

### I Committed But Want to Undo (Before Pushing)

```bash
# Keep changes, undo commit
git reset --soft HEAD~1
# Now you can re-stage and re-commit differently

# Undo commit AND discard changes (⚠️ PERMANENT)
git reset --hard HEAD~1
```

---
chunk_id: cli::english-guide::vectorization::001
domain: cli
chunk_type: guide
category: vectorization
confidence: high
reuse_level: universal
tags: [vectorization, english, guide, cli, workflow]
source_file: CLI_CHEATSHEET.md
---

# Vectorization Workflow

## What is Vectorization?

Converting your markdown guides into **searchable chunks** so you can query them later:

```
Markdown File → Split into Chunks → Convert to Vectors → Store in Pinecone
```

## Vectorize a Single File

```bash
# From repo root
cd /home/kali/Desktop/RAG

# Vectorize ONE markdown file
python3 src/vectorize_canonical_openai.py \
  ./docs/my-guide.md

# Check it worked
echo "Vectorization complete! Query it later with:"
echo "python3 src/query_canonical_openai.py 'search term'"
```

## Vectorize an Entire Directory

```bash
# Vectorize ALL files in docs/
python3 src/vectorize_canonical_openai.py \
  ./docs/

# Vectorize the entire repo
python3 src/vectorize_canonical_openai.py \
  .
```

## Vectorize New Files (After Adding to Git)

**Recommended workflow:**

```bash
# 1. Add new guide
nano docs/new-guide.md

# 2. Add to git
git add docs/new-guide.md

# 3. Commit
git commit -m "docs: Add new exploitation guide"

# 4. Vectorize the file
python3 src/vectorize_canonical_openai.py ./docs/new-guide.md

# 5. Push to GitHub
git push origin main

# 6. Now query it
python3 src/query_canonical_openai.py "guide topic"
```

---
chunk_id: cli::english-guide::push-pull::001
domain: cli
chunk_type: guide
category: git-remote
confidence: high
reuse_level: universal
tags: [git, push, pull, github, remote, english]
source_file: CLI_CHEATSHEET.md
---

# Uploading to Remote (GitHub)

## The Push-Pull Workflow

### Push Your Changes to GitHub

```bash
# After committing locally, push to main branch
git push origin main

# Check it worked
git status
# Should show: "Your branch is up to date with 'origin/main'"
```

### Pull Changes from GitHub (If Others Changed It)

```bash
# Fetch latest from GitHub
git fetch origin

# See what changed
git log HEAD..origin/main --oneline

# Pull (download and merge)
git pull origin main

# Or faster one-liner
git pull
```

## Full "One Person Workflow"

```bash
# 1. Start your day - get latest
git pull

# 2. Make changes
# ... edit files ...

# 3. Check what changed
git status

# 4. Stage all changes
git add .

# 5. Commit with message
git commit -m "feat: Add new exploitation guide"

# 6. Push to GitHub
git push

# 7. Verify
git log --oneline -3
```

---
chunk_id: cli::english-guide::quick-reference::001
domain: cli
chunk_type: reference
category: git-and-cli
confidence: high
reuse_level: universal
tags: [quick-reference, commands, english, cheatsheet]
source_file: CLI_CHEATSHEET.md
---

# Quick Reference Card

| Task | Command |
|------|---------|
| **Check Status** | `git status` |
| **See Changes** | `git diff` |
| **Stage All** | `git add .` |
| **Commit** | `git commit -m "msg"` |
| **Push** | `git push origin main` |
| **Pull** | `git pull origin main` |
| **View History** | `git log --oneline -10` |
| **Undo Last Commit** | `git reset --soft HEAD~1` |
| **Discard Changes** | `git restore .` |
| **Vectorize File** | `python3 src/vectorize_canonical_openai.py ./docs/file.md` |
| **Vectorize Dir** | `python3 src/vectorize_canonical_openai.py ./docs/` |
| **Query KB** | `python3 src/query_canonical_openai.py "search"` |
| **Copy Directory** | `cp -r source/ dest/` |
| **Remove File** | `git rm file.md` |
| **Revert Commit** | `git revert commit-hash` |

