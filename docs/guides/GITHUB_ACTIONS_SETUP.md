# GitHub Actions Setup Guide for Atlas Engine

**Complete beginner-friendly guide to automate your Atlas RAG application with GitHub Actions.**

---

## Table of Contents

1. [What is GitHub Actions?](#what-is-github-actions)
2. [Prerequisites](#prerequisites)
3. [Step 1: Add Your API Keys as Secrets](#step-1-add-your-api-keys-as-secrets)
4. [Step 2: Understanding Your Workflow](#step-2-understanding-your-workflow)
5. [Step 3: Running Tests from GitHub Web](#step-3-running-tests-from-github-web)
6. [Step 4: Running Tests from Command Line (Local)](#step-4-running-tests-from-command-line)
7. [What Each Test Does](#what-each-test-does)
8. [Troubleshooting](#troubleshooting)
9. [Safety First: Never Break Production](#safety-first-never-break-production)

---

## What is GitHub Actions?

GitHub Actions is a **free automation tool** that runs your code in the cloud whenever something happens to your repository (like pushing code). Think of it as a robot that:

- Builds your Docker image automatically
- Runs tests to make sure everything works
- Reports if anything breaks
- All for free!

**In our case:** Every time you push code to `main` branch, GitHub will:
1. Build your Docker container
2. Test that Atlas starts up correctly
3. Run a full integration test (query, ask, fetch, vectorize, delete)
4. Report success or failure

---

## Prerequisites

Before you start, make sure you have:

- ✅ A GitHub account
- ✅ Your repository pushed to GitHub (with `.github/workflows/docker-ci.yml` file already there)
- ✅ An OpenAI API key (for GPT)
- ✅ A Pinecone API key (for vector database)
- ✅ Admin access to your GitHub repository settings

**Don't have these keys yet?**
- OpenAI: Visit https://platform.openai.com/account/api-keys
- Pinecone: Visit https://www.pinecone.io/ and create a free account

---

## Step 1: Add Your API Keys as Secrets

**Important:** Never put API keys directly in code or config files. GitHub Secrets keeps them safe!

### From GitHub Web (Easiest for Beginners)

1. Go to your repository on GitHub.com
2. Click **Settings** (top right, gear icon)

   ```
   Your Repo > Settings
   ```

3. Click **Secrets and variables** > **Actions** (left sidebar)

   ```
   Settings > Secrets and variables > Actions
   ```

4. Click **New repository secret** (green button)

5. For **OPENAI_API_KEY**:
   - **Name:** `OPENAI_API_KEY`
   - **Secret:** Paste your OpenAI API key (keep it secret!)
   - Click **Add secret**

   ```
   Example (don't use this!):
   sk-proj-abc123def456...
   ```

6. Repeat for **PINECONE_API_KEY**:
   - **Name:** `PINECONE_API_KEY`
   - **Secret:** Paste your Pinecone API key
   - Click **Add secret**

**Result:** Your secrets are now safe in GitHub. The Actions workflow will use them automatically.

---

## Step 2: Understanding Your Workflow

Your workflow file is here: `.github/workflows/docker-ci.yml`

**What does it do?**

```
┌─────────────────────────────────────────┐
│  YOU PUSH CODE TO main BRANCH           │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  [STEP 1] Build Docker image            │
│  - Creates atlas-engine:ci container    │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  [STEP 2] Smoke test                    │
│  - Checks Atlas imports correctly       │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  [STEP 3] Integration test (IF secrets) │
│  - Ask GPT "What is LFI?"               │
│  - Query ffuf cheatsheet                │
│  - Ask GPT again (test cache)           │
│  - Fetch a chunk                        │
│  - Create test chunk + vectorize        │
│  - Delete test chunk                    │
│  - Clean up                             │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  [STEP 4] Push to GHCR (if main)        │
│  - Publishes docker image publicly      │
│  - Only on main branch                  │
└─────────────────────────────────────────┘
```

**Why is it safe?**
- Tests run in an **isolated namespace** (`ci-{run_id}`)
- Test data is **deleted automatically** after each run
- Your production data stays **untouched**
- If tests fail, they don't break your app

---

## Step 3: Running Tests from GitHub Web

### Option A: Automatically (When You Push Code)

1. Make a change to your code (any file in your repo)
2. Commit and push to the `main` branch:

   ```bash
   git add .
   git commit -m "Update Atlas"
   git push origin main
   ```

3. Go to your repository on GitHub.com
4. Click **Actions** tab (top of the page)

   ```
   Code | Pull requests | Actions | Projects
   ```

5. You'll see your workflow running! It shows:
   - 🔄 In Progress (yellow)
   - ✅ Success (green)
   - ❌ Failed (red)

6. Click on the workflow run to see details

   ```
   Docker CI > 1 min ago > ✅ Success
   ```

7. Click **build-and-smoke-test** to expand and see output

### Option B: Manually Trigger Workflow (Anytime You Want)

1. Go to your repository
2. Click **Actions** tab
3. Click **Docker CI** (left sidebar)

   ```
   All workflows
   └─ Docker CI
   ```

4. Click **Run workflow** (blue button)

   ```
   Run workflow ▼
   ```

5. Keep defaults and click **Run workflow** again

6. Your test starts immediately! Watch the progress in real-time.

---

## Step 4: Running Tests from Command Line (Local)

### If You Want to Test Locally First

Before pushing to GitHub, test your changes locally:

```bash
# 1. Go to your repo directory
cd /home/kali/Desktop/RAG

# 2. Build the Docker image
docker build -t atlas-engine:local .

# 3. Run the integration test
docker run --rm \
  -e ATLAS_CI_NAMESPACE="ci-local-test" \
  -v "/home/kali/Desktop/RAG/.env:/app/.env:ro" \
  atlas-engine:local src/ci_integration.py
```

**What this does:**
- Builds your Docker image locally
- Runs the same tests that GitHub Actions will run
- Uses your real API keys (mounted as read-only)
- Tests in a safe namespace `ci-local-test`

**If it succeeds locally, it will succeed on GitHub too!**

---

## What Each Test Does

### Test 1: Build Docker Image

```
⏱️  Time: ~2-3 minutes
💾 What: Creates a Docker container with all your code
✅ Success: You see "exporting layers" message
```

### Test 2: Smoke Test

```
⏱️  Time: ~5 seconds
🧪 What: Checks that Atlas imports and initializes correctly
✅ Success: You see "smoke-ok"
❌ Failure: Import error or dependency missing
```

### Test 3: Integration Test (Full Workflow)

**Only runs if you added API key secrets!**

```
⏱️  Time: ~30-60 seconds
🧪 What:
  [1/7] Ask GPT "What is LFI?"
        - Tests GPT backend
        - Uses your real Pinecone index
        - Tests answer generation

  [2/7] Query "ffuf cheatsheet"
        - Tests semantic search
        - Searches your default namespace
        - Should find 3 results

  [3/7] Ask GPT again "What is LFI?"
        - Tests caching
        - Should be instant (cached response)

  [4/7] Fetch a chunk
        - Tests fetch by ID
        - Retrieves known chunk: ffuf-cheatsheet
        - Displays chunk metadata

  [5/7] Create + Vectorize test chunk
        - Creates temporary .md file
        - Vectorizes into ci-{run_id} namespace
        - Tests embedding and Pinecone upload

  [6/7] Delete test chunk
        - Deletes the test chunk
        - Cleans up Pinecone
        - Tests deletion API

  [7/7] Done
        - Cleanup temp files
        - Report success

✅ Success: All 7 steps complete with no errors
❌ Failure: One step fails (see error message)
```

### Test 4: Push to GHCR (Container Registry)

```
⏱️  Time: ~2-3 minutes
🐳 What: Pushes your Docker image to GitHub Container Registry
📍 Location: ghcr.io/your-username/your-repo:latest
✅ Only runs: When pushing to main branch
```

---

## Troubleshooting

### Problem: "Workflow is not showing up in Actions tab"

**Cause:** The workflow file `.github/workflows/docker-ci.yml` might not be in the right place.

**Solution:**
```bash
# Make sure the file exists
ls -la .github/workflows/docker-ci.yml

# If not, push it to GitHub
git add .github/workflows/docker-ci.yml
git commit -m "Add Docker CI workflow"
git push origin main
```

Then wait 30 seconds and refresh the Actions tab.

---

### Problem: "Integration test says SKIPPED"

**Cause:** You haven't added API key secrets yet.

**Solution:** Follow [Step 1](#step-1-add-your-api-keys-as-secrets) to add `OPENAI_API_KEY` and `PINECONE_API_KEY` secrets.

---

### Problem: "Integration test fails with API error"

**Possible causes:**

1. **API key is wrong or expired**
   - Go to Settings > Secrets and variables > Actions
   - Update `OPENAI_API_KEY` or `PINECONE_API_KEY`
   - Run workflow again

2. **API key has no credit/quota**
   - OpenAI: Check your account at https://platform.openai.com/account/billing/overview
   - Pinecone: Check your usage at https://app.pinecone.io

3. **Pinecone index doesn't exist**
   - Make sure your Pinecone index is created
   - Default name: `rag-canonical-v1-emb3large`
   - Check in Pinecone console

---

### Problem: "Docker build fails"

**Cause:** Your dependencies or Python code has an issue.

**Solution:**
1. Test locally first:
   ```bash
   docker build -t atlas-engine:local .
   ```

2. If that fails, check error message carefully

3. Fix the issue and commit:
   ```bash
   git add .
   git commit -m "Fix Docker build"
   git push origin main
   ```

---

### Problem: "I accidentally broke something, how do I revert?"

**Solution 1: Revert last commit (safe)**
```bash
git revert HEAD --no-edit
git push origin main
```

**Solution 2: Go back to previous version**
```bash
git log --oneline
# Find the commit you want to go back to
git reset --hard abc1234  # Replace with commit hash
git push --force origin main
```

---

## Safety First: Never Break Production

### Golden Rules

1. **Always test locally first**
   ```bash
   docker build -t atlas-engine:local .
   docker run --rm -e ATLAS_CI_NAMESPACE="ci-test" \
     -v "./.env:/app/.env:ro" \
     atlas-engine:local src/ci_integration.py
   ```

2. **Never commit API keys**
   - Always use GitHub Secrets
   - Always use `.env/` directory (already in `.gitignore`)

3. **Tests use isolated namespace**
   - All test writes go to `ci-{run_id}` namespace
   - Your production data (`__default__` namespace) is safe
   - Test data is deleted automatically

4. **Commits to main branch always trigger tests**
   - Never force-push to main without testing
   - Review changes before committing
   - Use Pull Requests for bigger changes

---

## Typical Workflow: Step by Step

### Day-to-Day Workflow (Safest Way)

```
1. Make changes to your code
   ├─ Edit atlas_engine/chat.py
   ├─ Edit config.py
   └─ Add new chunk files

2. Test locally
   ├─ Build: docker build -t atlas-engine:local .
   └─ Run: docker run --rm -v "./.env:/app/.env:ro" ...

3. If local tests pass, commit
   ├─ git add .
   ├─ git commit -m "Describe your change"
   └─ git push origin main

4. GitHub Actions automatically tests on main
   ├─ Build Docker image
   ├─ Smoke test
   ├─ Integration test
   └─ Push to GHCR

5. Check GitHub Actions tab for results
   ├─ ✅ All green = Success!
   └─ ❌ Any red = Something broke (see logs)
```

### Example: Updating a Chunk File

```bash
# 1. Edit a chunk file
nano default/web/recon/injection-surface-mapping_sqli_001.md

# 2. Save changes (Ctrl+O, Enter, Ctrl+X)

# 3. Test locally
docker build -t atlas-engine:local .
docker run --rm -e ATLAS_CI_NAMESPACE="ci-test" \
  -v "./.env:/app/.env:ro" \
  atlas-engine:local src/ci_integration.py

# 4. If tests pass, commit
git add default/web/recon/injection-surface-mapping_sqli_001.md
git commit -m "Update SQLi chunk with new findings"
git push origin main

# 5. Watch GitHub Actions (Actions tab)
# Wait for ✅ All checks passed
```

### Example: Adding New Feature

```bash
# 1. Create feature branch (optional but recommended)
git checkout -b feature/new-graphrag

# 2. Make changes
vim atlas_engine/graph.py  # Add new code

# 3. Test locally
docker build -t atlas-engine:local .
docker run --rm -v "./.env:/app/.env:ro" atlas-engine:local python -c \
  "from atlas_engine import Atlas; print('Feature works')"

# 4. Push to GitHub (same branch)
git add atlas_engine/graph.py
git commit -m "Add GraphRAG support"
git push origin feature/new-graphrag

# 5. Create Pull Request
#    - Go to GitHub.com
#    - Click "Compare & pull request"
#    - Add description
#    - Click "Create pull request"

# 6. GitHub runs tests on the PR automatically
#    - See results in PR page
#    - Fix any failures
#    - Once green, merge to main

# 7. After merge, GitHub runs full tests on main
#    - Build, smoke test, integration test, publish
```

---

## Monitoring Your Tests

### From GitHub Web

1. Go to Actions tab
2. See list of all workflow runs
3. Click any run to see details

**Understanding the status:**
- 🟡 **Yellow circle** = Running
- 🟢 **Green checkmark** = Success
- 🔴 **Red X** = Failed
- ⏭️ **Skipped** = Conditions not met (e.g., no secrets)

### From Command Line

```bash
# See last 5 workflow runs
gh run list --limit 5

# See details of a specific run
gh run view <run-id>

# See logs of a workflow
gh run view <run-id> --log

# Check workflow status
gh workflow list
```

**Note:** You need GitHub CLI installed. Install with:
```bash
# macOS
brew install gh

# Linux
curl -sL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh

# Windows (with Scoop)
scoop install gh
```

---

## Advanced: Customizing Your Workflow

### Running Tests Only on Pull Requests (Not Main Commits)

Edit `.github/workflows/docker-ci.yml`:

```yaml
on:
  pull_request:
  # Remove this line if you don't want automatic main pushes
  # push:
  #   branches:
  #     - main
```

### Running Tests on Different Branches

```yaml
on:
  push:
    branches:
      - main
      - develop
      - staging
```

### Scheduling Tests (Nightly)

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Every day at 2 AM UTC
```

### Manual Trigger (Run Anytime)

```yaml
on:
  workflow_dispatch:
```

Then go to Actions > Docker CI > Run workflow button.

---

## Quick Reference Cheatsheet

| Task | Command/Steps |
|------|---------------|
| **Add API secret** | Settings > Secrets and variables > Actions > New secret |
| **Run workflow manually** | Actions > Docker CI > Run workflow |
| **View workflow logs** | Actions > Click run > Expand job step |
| **Test locally** | `docker build -t atlas-engine:local . && docker run --rm -v "./.env:/app/.env:ro" atlas-engine:local src/ci_integration.py` |
| **Check workflow status** | `gh run list` |
| **View last run logs** | `gh run view --log` |
| **Revert last commit** | `git revert HEAD && git push origin main` |
| **View secrets** | Settings > Secrets and variables > Actions |
| **Update secret** | Delete old, create new one (same name) |

---

## Summary

**You now know:**

✅ What GitHub Actions is (automated testing in the cloud)
✅ How to add API keys securely (GitHub Secrets)
✅ How to run tests from GitHub web (Actions tab)
✅ How to run tests locally first (Docker)
✅ What each test does (build, smoke, integration, publish)
✅ How to troubleshoot failures (common issues)
✅ How to keep your app safe (isolated namespaces, auto-cleanup)

**Next time you make changes:**

1. Edit your code
2. Test locally: `docker build ... && docker run ...`
3. Commit: `git add . && git commit && git push origin main`
4. Watch: Go to Actions tab
5. Celebrate: 🎉 If all green!

---

## Need More Help?

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **Docker Docs:** https://docs.docker.com/
- **Your Workflow File:** `.github/workflows/docker-ci.yml`
- **Integration Script:** `src/ci_integration.py`

**Questions?** Comment in your repo or check the Troubleshooting section above!

---

**Last updated:** February 2026
**Atlas Engine Version:** 2.0+
