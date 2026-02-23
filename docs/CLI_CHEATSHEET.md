---
title: "CLI Cheatsheet: CTF Bug Hunter Retrieval System"
desc: "Complete CLI command reference for CTF Bug Hunter Repository - Git operations, file management, vectorization workflow, and directory operations"
author: "CTF Community"
created: 2026-02-20
updated: 2026-02-20
tags: ["cli", "git", "vectorization", "cheatsheet", "commands", "guide"]
namespace: "cli-commands-guide"
---

# CLI Cheatsheet: CTF Bug Hunter Retrieval System

> **Cheatcode Mode Activated** 🔥 - Everything you need to work with the repo. No fluff, straight to the point.

---

## Table of Contents

1. [Absolute Beginner Setup](#absolute-beginner-setup)
2. [Git Basics (Track Changes)](#git-basics-track-changes)
3. [Making Changes (Edit & Commit)](#making-changes-edit--commit)
4. [Reverting & Fixing Mistakes](#reverting--fixing-mistakes)
5. [Directory & File Operations](#directory--file-operations)
6. [Uploading to Remote (GitHub)](#uploading-to-remote-github)
7. [Vectorization Workflow](#vectorization-workflow)
8. [Script Reference Quick Fire](#script-reference-quick-fire)

---

## Absolute Beginner Setup

### First Time Setup (Copy-Paste Ready)

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

### Verify You're Ready

```bash
# Should show: On branch main, nothing to commit
git status

# Should show your commits
git log --oneline -5
```

---

## Git Basics (Track Changes)

### Understanding Git States

```
WORKING DIR → STAGING AREA → LOCAL REPO → GITHUB
   (files)      (git add)    (git commit)  (git push)
```

### Check What Changed

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

### Stage Files for Commit

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

### Commit (Save Locally)

```bash
# Simple commit
git commit -m "Fixed typo in README"

# Better commit (with details)
git commit -m "Fix: Update vectorizer instructions for Python 3.10
- Added virtual environment activation steps
- Clarified dependency installation
- Added troubleshooting section"

# Commit everything in one go
git add . && git commit -m "feat: Add new CTF guide for SQL injection"

# Check your commits
git log --oneline -10
```

### Commit Message Format (Pro Tips)

```
Fix: Brief description
Feat: New feature added
Docs: Documentation updates
Refactor: Code restructuring
Test: Test additions
```

---

## Making Changes (Edit & Commit)

### Workflow: Change → Stage → Commit → Push

#### Example 1: Edit a Markdown File

```bash
# 1. Open and edit the file
nano docs/guides/my-guide.md
# (Or use your editor: vim, code, gedit, etc.)

# 2. Check what changed
git diff docs/guides/my-guide.md

# 3. Stage it
git add docs/guides/my-guide.md

# 4. Commit it
git commit -m "docs: Improve CTF SQL injection guide with examples"

# 5. Push to GitHub
git push origin main
```

#### Example 2: Add a New File

```bash
# 1. Create the file
echo "# My New Guide" > docs/guides/new-guide.md

# 2. Add content (use your editor)
nano docs/guides/new-guide.md

# 3. Stage it
git add docs/guides/new-guide.md

# 4. Commit it
git commit -m "docs: Add new guide for API enumeration techniques"

# 5. Push
git push origin main
```

#### Example 3: Add Multiple Files at Once

```bash
# 1. Create several files
echo "Content 1" > docs/api-1.md
echo "Content 2" > docs/api-2.md
echo "Content 3" > docs/api-3.md

# 2. Stage all
git add .

# 3. Commit them together
git commit -m "docs: Add API enumeration documentation (3 new guides)"

# 4. Push
git push origin main
```

### Check Your Progress

```bash
# See local commits not yet pushed
git log origin/main..HEAD --oneline

# See commits on GitHub not yet pulled
git log HEAD..origin/main --oneline

# See full history
git log --graph --oneline --all
```

---

## Reverting & Fixing Mistakes

### "Oops, I Didn't Mean That" - Recovery Guide

#### I Edited a File But Haven't Staged It

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

#### I Staged Files But Want to Unstage

```bash
# Unstage ONE file
git reset filename.md

# Unstage ALL files
git reset

# Verify
git status
```

#### I Committed But Want to Undo (Before Pushing)

```bash
# Keep changes, undo commit
git reset --soft HEAD~1
# Now you can re-stage and re-commit differently

# Undo commit AND discard changes (⚠️ PERMANENT)
git reset --hard HEAD~1
```

#### I Pushed to GitHub and Need to Undo (⚠️ DANGER)

```bash
# See the commit you want to undo
git log --oneline -5

# Create a NEW commit that reverses it
git revert commit-hash-here
# This creates a new commit that undoes the changes

# Push the revert
git push origin main
```

#### I Committed with Wrong Message

```bash
# Fix ONLY the last commit message (before push)
git commit --amend -m "Fixed message here"

# Push the corrected commit
git push origin main
```

#### "Nuclear Option" - Discard Everything

```bash
# Discard ALL changes and go back to last commit
git reset --hard HEAD

# Go back to last pushed state
git reset --hard origin/main
```

---

## Directory & File Operations

### Working with Multiple Files

#### Upload a Whole Directory

```bash
# Copy a directory into the repo
cp -r /path/to/my/ctf-notes /home/kali/Desktop/RAG/docs/

# OR create it in the repo
mkdir -p /home/kali/Desktop/RAG/docs/my-ctf-notes

# Add everything in that directory
git add docs/my-ctf-notes/

# Commit
git commit -m "docs: Add CTF notes for OWASP Top 10"

# Push
git push origin main
```

#### Upload Files into `default/` Directory

The `default/` directory is for example CTF chunks:

```bash
# Copy CTF chunks into default/
cp -r /path/to/ctf-chunks/* /home/kali/Desktop/RAG/default/

# Add to git
git add default/

# Commit
git commit -m "docs: Add example CTF chunks for X and Y machines"

# Push
git push origin main
```

#### Upload Files into `src/` (Python Scripts)

Only Python scripts go here:

```bash
# Copy new Python script
cp /path/to/my-script.py /home/kali/Desktop/RAG/src/

# Add it
git add src/my-script.py

# Commit
git commit -m "feat: Add new script for automated fuzzing"

# Update SCRIPTS_INDEX.md to document it
nano SCRIPTS_INDEX.md

# Re-add and commit
git add SCRIPTS_INDEX.md
git commit -m "docs: Document new fuzzing script"

# Push both
git push origin main
```

#### Upload Files into `scripts/` (Bash Scripts)

Only Bash CLI wrappers go here:

```bash
# Copy bash script
cp /path/to/my-script.sh /home/kali/Desktop/RAG/scripts/

# Make it executable
chmod +x /home/kali/Desktop/RAG/scripts/my-script.sh

# Add it
git add scripts/my-script.sh

# Commit
git commit -m "feat: Add bash wrapper for new fuzzing tool"

# Update documentation
nano SCRIPTS_INDEX.md

# Commit docs update
git add SCRIPTS_INDEX.md
git commit -m "docs: Document new bash wrapper"

# Push
git push origin main
```

#### Upload Files into `docs/` (Markdown Guides)

Guides go in organized subdirectories:

```bash
# Navigate to docs
cd /home/kali/Desktop/RAG/docs

# Create a new guide
nano docs/my-new-ctf-guide.md

# Or copy existing guides
cp /path/to/my-guide.md docs/

# From repo root, add them
git add docs/

# Commit
git commit -m "docs: Add guide for [topic] exploitation"

# Push
git push origin main
```

### List Everything You Have

```bash
# See all files in repo
ls -la

# See structure
tree -L 2

# See only modified files
git status

# Count files
find . -type f | wc -l

# See size of repo
du -sh .
```

### Delete Files (If Needed)

```bash
# Delete a file and stage the deletion
git rm filename.md

# Delete a directory
git rm -r directory-name/

# Commit the deletion
git commit -m "docs: Remove outdated guide"

# Push
git push origin main
```

---

## Uploading to Remote (GitHub)

### The Push-Pull Workflow

#### Push Your Changes to GitHub

```bash
# After committing locally, push to main branch
git push origin main

# Check it worked
git status
# Should show: "Your branch is up to date with 'origin/main'"
```

#### Pull Changes from GitHub (If Others Changed It)

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

#### Handle Conflicts (Two People Edited Same File)

```bash
# Try to pull
git pull origin main

# If conflict:
# 1. Open the conflicted file
nano conflicted-file.md

# 2. Look for these markers:
# <<<<<<< HEAD (your changes)
# ======= (divider)
# >>>>>>> origin/main (their changes)

# 3. Edit to keep what you want, delete conflict markers

# 4. Stage and commit
git add conflicted-file.md
git commit -m "fix: Resolve merge conflict in [file]"

# 5. Push
git push origin main
```

### Full "One Person Workflow"

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

## Vectorization Workflow

### What is Vectorization?

Converting your markdown guides into **searchable chunks** so you can query them later:

```
Markdown File → Split into Chunks → Convert to Vectors → Store in Pinecone
```

### Vectorize a Single File

```bash
# From repo root
cd /home/kali/Desktop/RAG

# Vectorize ONE markdown file
python3 src/vectorize_canonical_openai.py \
  --file docs/my-guide.md \
  --namespace ctf-guides

# Check it worked
echo "Vectorization complete! Query it later with:"
echo "python3 src/query_canonical_openai.py 'search term'"
```

### Vectorize an Entire Directory

```bash
# Vectorize ALL files in docs/
python3 src/vectorize_canonical_openai.py \
  --directory docs/ \
  --namespace ctf-guides

# Vectorize the entire repo
python3 src/vectorize_canonical_openai.py \
  --directory . \
  --namespace ctf-all

# Progress output:
# Processing: docs/guides/sql-injection.md ... ✓
# Processing: docs/guides/xss-attacks.md ... ✓
# Created 45 chunks | Stored in Pinecone
```

### Vectorize New Files (After Adding to Git)

**Recommended workflow:**

```bash
# 1. Add new guide
nano docs/new-guide.md

# 2. Add to git
git add docs/new-guide.md

# 3. Commit
git commit -m "docs: Add new exploitation guide"

# 4. Vectorize the file
python3 src/vectorize_canonical_openai.py \
  --file docs/new-guide.md \
  --namespace ctf-guides

# 5. Push to GitHub
git push origin main

# 6. Now query it
python3 src/query_canonical_openai.py "guide topic"
```

### Vectorize the CLI Cheatsheet (THIS FILE!)

```bash
# Vectorize this guide
python3 src/vectorize_canonical_openai.py \
  --file CLI_CHEATSHEET.md \
  --namespace cli-commands

# Test a query
python3 src/query_canonical_openai.py "how to revert a commit"

# Should return relevant sections from this guide!
```

### Vectorize Everything at Once

```bash
# One-shot: commit + vectorize + push
git add .
git commit -m "docs: Major documentation update"
python3 src/vectorize_canonical_openai.py --directory . --namespace all
git push origin main
```

### Batch Vectorize Multiple Directories

```bash
# Script to vectorize multiple parts separately

# Vectorize guides
python3 src/vectorize_canonical_openai.py \
  --directory docs/ \
  --namespace guides

# Vectorize vectorizer docs
python3 src/vectorize_canonical_openai.py \
  --directory docs-vectorizer/ \
  --namespace vectorizer-guides

# Vectorize example chunks
python3 src/vectorize_canonical_openai.py \
  --directory default/ \
  --namespace example-chunks

# Vectorize CLI guide
python3 src/vectorize_canonical_openai.py \
  --file CLI_CHEATSHEET.md \
  --namespace cli-guide
```

---

## Script Reference Quick Fire

### Most-Used Commands

```bash
# Check git status
git status

# See what changed
git diff

# Stage all changes
git add .

# Commit
git commit -m "msg"

# Push to GitHub
git push

# Pull latest
git pull

# See history
git log --oneline -10

# Vectorize files
python3 src/vectorize_canonical_openai.py --directory docs/ --namespace guides

# Query knowledge base
python3 src/query_canonical_openai.py "your question"

# Send to Telegram
python3 src/rag_to_telegram.py "your query"
```

### File Operations Cheatsheet

```bash
# Create directory
mkdir -p path/to/new/dir

# Copy file
cp source.md dest.md

# Copy directory
cp -r source/ dest/

# Move/rename
mv old-name.md new-name.md

# List files
ls -la

# See directory tree
tree -L 3

# Remove file
rm filename.md

# Remove directory
rm -r directory/

# Find files
find . -name "*.md"

# Count files
find . -name "*.md" | wc -l
```

### Git Magic Shortcuts

Create in `~/.bashrc` or `~/.zshrc`:

```bash
# Add to your shell config file
alias gs='git status'
alias ga='git add .'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline -10'
alias gd='git diff'
alias gca='git add . && git commit -m'
alias gcap='git add . && git commit -m "$1" && git push'

# Then use:
# gs (instead of git status)
# gc "my message" (instead of git commit -m)
# gcap "my message" (stage, commit, and push in one!)
```

---

## Common Scenarios & Solutions

### Scenario 1: "I Made Changes, Want to Save Them"

```bash
git add .
git commit -m "feat: Describe your changes"
git push origin main
```

### Scenario 2: "I Made Changes, Want to Discard Them"

```bash
git restore .
# OR
git reset --hard HEAD
```

### Scenario 3: "I Committed Locally But Forgot to Push"

```bash
git log origin/main..HEAD --oneline  # See commits not pushed
git push origin main                 # Push them
```

### Scenario 4: "I Want to Vectorize My New Guide"

```bash
git add docs/my-new-guide.md
git commit -m "docs: Add new guide"
python3 src/vectorize_canonical_openai.py --file docs/my-new-guide.md --namespace guides
git push origin main
```

### Scenario 5: "I Want to Query My Vectorized Guides"

```bash
python3 src/query_canonical_openai.py "What is SQL injection?"
# Gets all relevant sections from vectorized guides!
```

### Scenario 6: "I Want to Add CTF Chunks to default/"

```bash
cp -r ~/my-ctf-chunks/* /home/kali/Desktop/RAG/default/
git add default/
git commit -m "docs: Add CTF chunks for machines X, Y, Z"
python3 src/vectorize_canonical_openai.py --directory default/ --namespace ctf-chunks
git push origin main
```

### Scenario 7: "I Pushed Something Wrong, Need to Undo"

```bash
git log --oneline -3              # Find the bad commit
git revert bad-commit-hash         # Create a undo commit
git push origin main               # Push the undo
```

---

## Environment & Dependencies

### Check Python Setup

```bash
# Verify Python 3 installed
python3 --version

# Verify required packages
python3 -c "import openai, pinecone; print('✓ Dependencies OK')"

# Install requirements
python3 -m pip install -r config/requirements.txt

# Verify venv (if using)
which python3
```

### Check API Keys Setup

```bash
# Pinecone API
echo $PINECONE_API_KEY

# OpenAI API
echo $OPENAI_API_KEY

# If empty, set them:
export PINECONE_API_KEY="your-key"
export OPENAI_API_KEY="your-key"

# Or use .env files (recommended):
# Create config/.env with your keys
```

### Check Git Configuration

```bash
# See your config
git config --list

# Set user info
git config user.name "Your Name"
git config user.email "your@email.com"

# Make global (all repos)
git config --global user.name "Your Name"
```

---

## Troubleshooting

### "Git says I have uncommitted changes"

```bash
# See what changed
git status

# Review changes
git diff

# Stage them
git add .

# Commit them
git commit -m "message"
```

### "Can't push to GitHub"

```bash
# Check connection
git remote -v

# Try pulling first
git pull origin main

# Then push
git push origin main
```

### "Python script not found"

```bash
# Make sure you're in repo root
pwd
# Should be /home/kali/Desktop/RAG

# Check file exists
ls src/vectorize_canonical_openai.py

# Run with full path
python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py --help
```

### "Vectorization failing"

```bash
# Check API keys
echo $OPENAI_API_KEY
echo $PINECONE_API_KEY

# Check dependencies
python3 -m pip list | grep -E "openai|pinecone"

# Check file format
file docs/my-guide.md  # Should be "ASCII text"

# Try verbose mode
python3 src/vectorize_canonical_openai.py \
  --file docs/my-guide.md \
  --namespace test \
  --verbose
```

---

## Pro Tips

### Tip 1: Commit Often, Push When Ready

```bash
# Commit locally multiple times
git commit -m "Work in progress"
git commit -m "Added section A"
git commit -m "Fixed bugs in section B"

# Push once when everything is good
git push origin main
```

### Tip 2: Use Descriptive Commit Messages

```bash
# Bad
git commit -m "update"

# Good
git commit -m "feat: Add SQL injection exploitation guide with payloads and bypass techniques"
```

### Tip 3: Vectorize After Every Major Update

```bash
# New guide? Vectorize it!
# Updated old guide? Re-vectorize!
# Added examples? Vectorize again!

# Query to verify
python3 src/query_canonical_openai.py "your topic"
```

### Tip 4: Use Aliases to Speed Up

```bash
alias vc='python3 src/vectorize_canonical_openai.py'
alias qc='python3 src/query_canonical_openai.py'

# Then:
vc --directory docs/ --namespace guides
qc "search term"
```

### Tip 5: Always Pull Before Working

```bash
# Start of session
git pull origin main

# Work
# ... edit files ...

# End of session
git push origin main
```

---

## Quick Reference Card

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
| **Vectorize File** | `python3 src/vectorize_canonical_openai.py --file docs/file.md --namespace ns` |
| **Vectorize Dir** | `python3 src/vectorize_canonical_openai.py --directory docs/ --namespace ns` |
| **Query KB** | `python3 src/query_canonical_openai.py "search"` |
| **Copy Directory** | `cp -r source/ dest/` |
| **Remove File** | `git rm file.md` |
| **Revert Commit** | `git revert commit-hash` |

---

## Final Checklist Before Using Repository

```bash
# ✓ Installed dependencies
python3 -m pip install -r config/requirements.txt

# ✓ Git configured
git config user.name "Your Name"
git config user.email "your@email.com"

# ✓ Can see status
git status

# ✓ Can see history
git log --oneline -5

# ✓ Have API keys
echo $OPENAI_API_KEY
echo $PINECONE_API_KEY

# ✓ Can run vectorizer
python3 src/vectorize_canonical_openai.py --help

# ✓ Can query
python3 src/query_canonical_openai.py --help

# YOU'RE READY TO GO! 🚀
```

---

**Last Updated**: February 2026  
**Repository**: https://github.com/Audionerdz/CTF-Bug-Hunter-Retrieval  
**Status**: Production Ready

