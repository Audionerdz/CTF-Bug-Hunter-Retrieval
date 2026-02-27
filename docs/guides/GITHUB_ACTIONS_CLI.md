# GitHub Actions: Command Line Guide

**Complete guide for developers who prefer terminal.**

---

## Prerequisites

You need:
- ✅ Git installed and configured
- ✅ GitHub CLI (`gh`) installed
- ✅ API keys (OpenAI, Pinecone)
- ✅ Repository cloned locally

---

## Installation

### Install GitHub CLI (if you don't have it)

**macOS:**
```bash
brew install gh
```

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh
```

**Windows (Scoop):**
```bash
scoop install gh
```

### Authenticate with GitHub

```bash
# Login with your GitHub account
gh auth login

# Choose:
# - Which host you're authenticating with? GitHub.com
# - What is your preferred protocol? HTTPS or SSH
# - Authenticate Git with your GitHub credentials? Yes
# - How would you like to authenticate GitHub CLI? Paste an authentication token
```

---

## Step 1: Add API Keys as Secrets (Command Line)

### Add OPENAI_API_KEY

```bash
# Get your OpenAI key first from: https://platform.openai.com/api-keys

gh secret set OPENAI_API_KEY --body "sk-proj-your-key-here"
```

**What it does:**
- Stores your OpenAI key securely in GitHub
- Shows: ✓ Secret OPENAI_API_KEY set for YOUR-USERNAME/YOUR-REPO

### Add PINECONE_API_KEY

```bash
# Get your Pinecone key first from: https://app.pinecone.io

gh secret set PINECONE_API_KEY --body "pcn-your-key-here"
```

**What it does:**
- Stores your Pinecone key securely in GitHub
- Shows: ✓ Secret PINECONE_API_KEY set for YOUR-USERNAME/YOUR-REPO

### Verify Secrets Were Added

```bash
gh secret list
```

**Output:**
```
OPENAI_API_KEY      Updated 1 minute ago
PINECONE_API_KEY    Updated 1 minute ago
```

### Update a Secret (if you need to)

```bash
# Delete old secret
gh secret delete OPENAI_API_KEY

# Add new secret with same name
gh secret set OPENAI_API_KEY --body "new-key-here"
```

---

## Step 2: Make Changes and Push

### Option A: Edit Files Locally

```bash
# 1. Navigate to your repo
cd /home/kali/Desktop/RAG

# 2. Make changes to any file
echo "# Updated" >> README.md

# 3. Stage changes
git add README.md

# 4. Commit
git commit -m "Update README for testing"

# 5. Push to GitHub
git push origin main
```

**What happens:**
- GitHub detects push to main
- Automatically triggers workflow
- Tests run automatically

---

### Option B: Edit Files and Push (One-Liner)

```bash
cd /home/kali/Desktop/RAG && \
  echo "# Updated" >> README.md && \
  git add README.md && \
  git commit -m "Test GitHub Actions" && \
  git push origin main
```

---

## Step 3: Watch Tests Run (Command Line)

### List Recent Workflow Runs

```bash
# See last 5 runs
gh run list --limit 5
```

**Output:**
```
STATUS  TITLE                           BRANCH  EVENT  AGE
✓       Update README for testing       main    push   1 minute ago
✓       Previous test                   main    push   5 minutes ago
✗       Failed deployment               main    push   1 hour ago
```

### View Details of Latest Run

```bash
# Show last run
gh run view
```

**Output:**
```
Run #123
Status: ✓ completed successfully

JOBS
build-and-smoke-test  ✓ completed in 4m 30s
Atlas integration flow  ✓ completed in 1m 20s
publish-ghcr           ✓ completed in 2m 40s
```

### View a Specific Run

```bash
# List runs
gh run list --limit 10

# View specific run by number
gh run view 123
```

---

## Step 4: See Full Test Logs

### View Last Run's Logs

```bash
# See last run
gh run view --log
```

**Output (partial):**
```
[build-and-smoke-test]
#0 building with "default" instance using docker driver
#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 734B done
...
DONE 0.1s
[smoke test]
RAG Framework v2.0
  Index: rag-canonical-v1-emb3large:__default__
  Chunks: 160
  Root: /app
smoke-ok
```

### View a Specific Run's Logs

```bash
gh run view 123 --log
```

### Watch Logs in Real-Time

```bash
# Watch last run (updates every 5 seconds)
gh run view --log --exit-status

# Watch specific run
gh run view 123 --log --exit-status
```

---

## Step 5: Trigger Workflow Manually

### Run Workflow Without Pushing Code

```bash
# Trigger workflow
gh workflow run docker-ci.yml
```

**What it does:**
- Starts a new workflow run immediately
- Runs latest code in main branch
- No code changes needed

### Check Workflow Was Triggered

```bash
# List runs (new one should be at top)
gh run list --limit 3
```

### Watch It Start

```bash
# View the run that just started
gh run view --log --exit-status
```

---

## Advanced: Check Specific Job Results

### View All Jobs in a Run

```bash
# View run with all jobs
gh run view 123
```

**Output:**
```
Run #123
Status: ✓ completed successfully

JOBS
✓ build-and-smoke-test  (4m 30s)
✓ Atlas integration flow  (1m 20s)
✓ publish-ghcr           (2m 40s)
```

### View Specific Job Logs

```bash
# Get logs for a specific job
gh run view 123 --log | grep -A 50 "Atlas integration flow"
```

---

## Advanced: Download Artifacts (if any)

```bash
# Download artifacts from a run
gh run download 123
```

---

## Continuous Monitoring

### Watch Tests Live (Polling)

```bash
# Poll every 10 seconds until complete
while true; do
  clear
  echo "=== Atlas Engine CI Status ==="
  gh run view --log --exit-status 2>/dev/null || echo "Still running..."
  echo "Last updated: $(date)"
  sleep 10
done
```

**Press Ctrl+C to stop**

---

## Troubleshooting from Command Line

### Check If Secrets Exist

```bash
gh secret list
```

**If empty, add secrets (see Step 1)**

---

### Check Workflow File Syntax

```bash
# Validate workflow YAML
cat .github/workflows/docker-ci.yml | yq . > /dev/null && echo "✓ Valid" || echo "✗ Invalid YAML"
```

**Or manually:**
```bash
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/docker-ci.yml'))" && echo "✓ Valid"
```

---

### View Workflow File

```bash
# Show workflow
cat .github/workflows/docker-ci.yml
```

---

### Re-Run a Failed Workflow

```bash
# Get the run ID
gh run list --limit 1

# Re-run it
gh run rerun <RUN_ID>
```

---

### Cancel a Running Workflow

```bash
# Get latest run
gh run list --limit 1

# Cancel it
gh run cancel <RUN_ID>
```

---

## Test Locally Before Pushing

### Always Test Locally First

```bash
# Go to your repo
cd /home/kali/Desktop/RAG

# Build Docker image
docker build -t atlas-engine:local .

# Run integration test
docker run --rm \
  -e ATLAS_CI_NAMESPACE="ci-local-test" \
  -v "/home/kali/Desktop/RAG/.env:/app/.env:ro" \
  atlas-engine:local src/ci_integration.py
```

**If this works locally, it will work on GitHub!**

---

## Complete CLI Workflow (Summary)

```bash
# 1. Setup (first time only)
gh auth login
gh secret set OPENAI_API_KEY --body "your-key"
gh secret set PINECONE_API_KEY --body "your-key"

# 2. Day-to-day development
cd /home/kali/Desktop/RAG
# ... edit your files ...
docker build -t atlas-engine:local .
docker run --rm -v "./.env:/app/.env:ro" atlas-engine:local src/ci_integration.py

# 3. If tests pass locally, push to GitHub
git add .
git commit -m "Your change description"
git push origin main

# 4. Watch tests on GitHub
gh run view --log --exit-status

# 5. All done! ✅
```

---

## Useful Aliases (Optional)

Add to your `.bashrc` or `.zshrc`:

```bash
# View last workflow run
alias gh-last='gh run view --log --exit-status'

# List recent runs
alias gh-runs='gh run list --limit 10'

# Trigger workflow
alias gh-test='gh workflow run docker-ci.yml'

# Check secrets
alias gh-secrets='gh secret list'

# Watch a specific run
gh-watch() {
  gh run view $1 --log --exit-status
}
```

Then use:
```bash
gh-last           # View last run
gh-runs           # List runs
gh-test           # Trigger test
gh-secrets        # Check secrets
gh-watch 123      # Watch run #123
```

---

## Quick Reference

| Command | What It Does |
|---------|--------------|
| `gh secret set NAME --body VALUE` | Add a secret |
| `gh secret list` | List all secrets |
| `gh run list` | List workflow runs |
| `gh run view` | View last run details |
| `gh run view --log` | View last run logs |
| `gh run view 123` | View specific run |
| `gh workflow run docker-ci.yml` | Trigger workflow manually |
| `gh run rerun 123` | Re-run a workflow |
| `gh run cancel 123` | Cancel a running workflow |
| `docker build -t atlas-engine:local .` | Build image locally |
| `docker run --rm -v "./.env:/app/.env:ro" atlas-engine:local src/ci_integration.py` | Run tests locally |

---

## Typical Day in Your Life

```bash
# Morning: Make changes
cd /home/kali/Desktop/RAG
nano atlas_engine/chat.py

# Before committing: Test locally
docker build -t atlas-engine:local .
docker run --rm -v "./.env:/app/.env:ro" atlas-engine:local src/ci_integration.py

# If tests pass, commit and push
git add atlas_engine/chat.py
git commit -m "Fix chat memory issue"
git push origin main

# Watch tests run (optional)
gh run view --log --exit-status

# When ready, check final status
gh run list --limit 1
```

---

## GitHub CLI Docs

For more commands:
```bash
gh --help
gh run --help
gh workflow --help
gh secret --help
```

Or visit: https://cli.github.com/manual/

---

**Last updated:** February 2026
**Atlas Engine Version:** 2.0+
