# GitHub Actions: Web Walkthrough (With Screenshots Descriptions)

**Visual step-by-step guide for GitHub.com web interface (no command line needed).**

---

## Overview

You'll do this **completely from your browser** without opening a terminal:

```
Step 1: Get your API keys (5 min)
   ↓
Step 2: Add keys to GitHub (5 min)
   ↓
Step 3: Push a change (manual or via web editor) (5 min)
   ↓
Step 4: Watch tests run in Actions tab (automatic)
   ↓
Done! ✅
```

Total time: **20 minutes** (first time setup)

---

## Part A: Get Your API Keys (5 minutes)

### Get OpenAI API Key

**Location:** https://platform.openai.com/api-keys

**Steps:**
1. Go to https://platform.openai.com/api-keys
2. Log in with your OpenAI account (or create one)
3. Click **"Create new secret key"** button
4. A popup shows your new key: `sk-proj-abc123...`
5. Click **Copy** button (icon with two overlapping rectangles)
6. **Paste it somewhere safe** (notepad, temporary file)
   - Don't close this window yet!
   - Keep this key private!

**Save this for Step 2: `OPENAI_API_KEY`**

---

### Get Pinecone API Key

**Location:** https://app.pinecone.io

**Steps:**
1. Go to https://app.pinecone.io
2. Log in with your Pinecone account (or create free account)
3. Click your **profile icon** (top right)
4. Click **"Copy API Key"** or similar option
5. A popup shows your key
6. Click **Copy** button
7. **Paste it somewhere safe** (notepad, temporary file)

**Save this for Step 2: `PINECONE_API_KEY`**

---

## Part B: Add Keys to GitHub (5 minutes)

### Step 1: Go to Your Repository Settings

**In your browser:**

1. Open your GitHub repository
   ```
   https://github.com/YOUR-USERNAME/YOUR-REPO-NAME
   ```

2. Look at the top of the page, you see tabs:
   ```
   Code | Issues | Pull requests | Discussions | Actions | ...
   ```

3. Look for **Settings** (usually far right, may need to click "...")
   - Or go directly to: `https://github.com/YOUR-USERNAME/YOUR-REPO-NAME/settings`

4. Click **Settings**

   **Visual:** You'll see a gear icon ⚙️ near the top right. Click it.

---

### Step 2: Go to Secrets Section

**On the Settings page:**

1. Look at the **left sidebar**. You see menu items:
   ```
   General
   Access
   Moderation
   Code and automation
   Secrets and variables  ← CLICK HERE
   ...
   ```

2. Click **Secrets and variables**

3. A submenu appears:
   ```
   Actions
   Dependabot
   Codespaces
   ```

4. Click **Actions**

   **Visual:** You're now at the "Actions secrets and variables" page.

---

### Step 3: Add First Secret (OPENAI_API_KEY)

**On the Actions secrets page:**

1. Look for the green button: **"New repository secret"**
2. Click it

3. A form appears with two fields:
   ```
   Name:     [____________________]
   Secret:   [____________________]
   ```

4. Fill in:
   - **Name:** Type exactly: `OPENAI_API_KEY`
   - **Secret:** Paste your OpenAI key (from Part A)

   **Example:**
   ```
   Name:   OPENAI_API_KEY
   Secret: sk-proj-abc123def456xyz...
   ```

5. Click **"Add secret"** button (green)

   **Visual:** The secret appears in the list below with a green checkmark ✅

---

### Step 4: Add Second Secret (PINECONE_API_KEY)

**Still on the Actions secrets page:**

1. Click **"New repository secret"** again

2. Fill in:
   - **Name:** Type exactly: `PINECONE_API_KEY`
   - **Secret:** Paste your Pinecone key (from Part A)

   **Example:**
   ```
   Name:   PINECONE_API_KEY
   Secret: pcn-abc123def456xyz...
   ```

3. Click **"Add secret"** button (green)

   **Visual:** Now you have two secrets listed:
   ```
   ✅ OPENAI_API_KEY    (Updated 1 minute ago)
   ✅ PINECONE_API_KEY  (Updated 1 minute ago)
   ```

**✅ Done!** Your secrets are safely stored in GitHub.

---

## Part C: Make a Change & Push (3 methods)

### Method 1: Edit Directly on GitHub Web (Easiest)

**Go to your repository:**

1. Go to `https://github.com/YOUR-USERNAME/YOUR-REPO-NAME`

2. Click **Code** tab (top of page)

3. Navigate to any file, e.g., `README.md`

4. Click the **pencil icon** ✏️ (top right of the file)

   **Visual:** You're now in "Edit mode"

5. Make a small change anywhere in the file:
   ```
   Add a line at the end:
   
   # Updated
   ```

6. Scroll to the bottom. You see:
   ```
   Commit changes
   [Description field]
   [Optional extended description field]
   [Commit directly to main branch]  ← SELECT THIS
   [Commit to a new branch...]
   ```

7. In the description field, type:
   ```
   Test GitHub Actions workflow
   ```

8. Make sure "Commit directly to main branch" is selected

9. Click **"Commit changes"** button (green)

   **Visual:** You're back at the file view. Change is committed!

---

### Method 2: Push from Command Line (If You Prefer)

**On your computer:**

```bash
# Go to your repo directory
cd /home/kali/Desktop/RAG

# Make a change
echo "# Updated by GitHub Actions" >> README.md

# Commit
git add README.md
git commit -m "Test GitHub Actions workflow"

# Push
git push origin main
```

**Done!** Your change is pushed to GitHub.

---

### Method 3: Use GitHub Desktop (GUI Alternative)

**If you have GitHub Desktop installed:**

1. Open GitHub Desktop
2. Click your repository
3. Make changes in your editor
4. See changes in GitHub Desktop
5. Click **Commit to main**
6. Click **Push origin**

---

## Part D: Watch Tests Run (Automatic)

### After you push (any method above):

**Go to your repository:**

1. Click the **Actions** tab (top of page)

   **Visual:** You see your workflow running!
   ```
   Workflow name: Docker CI
   Status: 🟡 In progress (yellow)
   "Build Docker image" or similar
   ```

2. Click on the workflow run to see details

3. You'll see multiple jobs:
   ```
   build-and-smoke-test    🟡 In progress...
   ```

4. Click on **build-and-smoke-test** to expand it

   **Visual:** You see steps:
   ```
   ✅ Checkout
   ✅ Set up Docker Buildx
   🟡 Build image (CI)  ← Currently running
   ```

5. **Wait for it to complete.** It takes:
   - ~3-5 minutes for Docker build
   - ~30 seconds for smoke test
   - ~30-60 seconds for integration test (if API keys added)

6. **When done,** you'll see:
   - ✅ All green checkmarks = SUCCESS!
   - 🔴 Any red X = FAILED (see error message)

---

## Part E: Understanding What Just Happened

### Workflow Timeline (What GitHub Ran)

```
TIME 0:00 - You clicked "Commit changes"
           ↓
TIME 0:10 - GitHub detected change in main branch
           ↓
TIME 0:20 - GitHub Actions triggered automatically
           ↓
TIME 1:00 - Download your code to GitHub servers
           ↓
TIME 2:00 - Docker build started (3-5 minutes)
           ↓
TIME 5:30 - Docker image created
           ↓
TIME 6:00 - Smoke test (checks Atlas imports) - 30 seconds
           ↓
TIME 6:30 - Integration test (your API keys) - 30-60 seconds
           ├─ [1/7] Ask GPT
           ├─ [2/7] Query ffuf
           ├─ [3/7] Ask GPT again (cache)
           ├─ [4/7] Fetch chunk
           ├─ [5/7] Vectorize test
           ├─ [6/7] Delete test
           └─ [7/7] Done
           ↓
TIME 7:30 - Publish Docker image to GHCR (2-3 minutes) (main branch only)
           ↓
TIME 9:00 - ALL TESTS COMPLETE ✅
```

---

## Part F: Viewing Test Results in Detail

### On the Actions Tab

1. Click **Actions** tab
2. See workflow history:
   ```
   Docker CI | Updated by GitHub Actions workflow - 2 min ago - ✅
   Docker CI | Previous commit - 5 days ago - ✅
   Docker CI | Old commit - 10 days ago - ❌
   ```

3. Click any workflow run to see details

4. You see jobs:
   ```
   build-and-smoke-test        ✅ Success in 4m 30s
   Atlas integration flow      ✅ Success in 1m 20s (only if secrets added)
   publish-ghcr                ✅ Success in 2m 40s (only on main)
   ```

5. Click on a job to expand and see individual steps:
   ```
   ✅ Checkout (0.2s)
   ✅ Set up Docker Buildx (1.5s)
   ✅ Build image (CI) (4m 20s)
   ✅ Smoke test container (30s)
   ✅ Prepare CI env files (0.1s)
   ✅ Atlas integration flow (1m 10s)
   ✅ Build and push image (2m 40s)
   ```

6. Click on any step to see its output:
   ```
   #0 building with "default" instance using docker driver
   #1 [internal] load build definition from Dockerfile
   #1 transferring dockerfile: 734B done
   ...
   [1/7] ask(gpt): What is LFI?
   answer chars=525 sources=4
   ...
   ```

---

## Part G: Fixing Common Issues (From Web)

### Issue 1: Integration Test Skipped

**You see:** ⏭️ "SKIPPED" on integration test step

**Cause:** API keys not added to GitHub Secrets

**Fix (from web):**
1. Go to Settings > Secrets and variables > Actions
2. Click **"New repository secret"**
3. Add missing keys (see Part B)
4. Go back to Actions tab
5. Click **"Run workflow"** button (blue)
6. Click **"Run workflow"** again
7. Tests will run immediately with your secrets

---

### Issue 2: Docker Build Failed

**You see:** 🔴 "Build image (CI)" step failed in red

**Cause:** There's an error in your code or dependencies

**Fix (from web):**
1. Click on the failed step to see error message
2. Read the error carefully
3. Go to your file and fix the issue
4. Commit the fix (using web editor or git push)
5. Workflow automatically runs again with your fix

---

### Issue 3: Integration Test Failed

**You see:** 🔴 One of the [X/7] steps failed

**Possible causes and fixes:**

**API key is wrong:**
- Go to Settings > Secrets
- Delete the key
- Click **"New repository secret"**
- Add it again (copy-paste carefully)

**API key has no credits:**
- Check OpenAI: https://platform.openai.com/account/billing/overview
- Check Pinecone: https://app.pinecone.io (usage)
- Add credits and try again

**Pinecone index doesn't exist:**
- Go to https://app.pinecone.io
- Create index named: `rag-canonical-v1-emb3large`
- Try workflow again

---

## Part H: Manual Workflow Trigger (Anytime)

**You don't have to commit code to run tests.**

### From GitHub Web:

1. Go to **Actions** tab
2. Click **Docker CI** (left sidebar)

   **Visual:**
   ```
   All workflows
   └─ Docker CI  ← Click here
   ```

3. Click **"Run workflow"** (blue dropdown button, top right)

   **Visual:** A dropdown appears:
   ```
   ▼ Run workflow
   ```

4. Click **"Run workflow"** (in the dropdown)

5. Tests start immediately! (you can watch in real-time)

---

## Part I: Scheduled Tests (Optional Advanced)

**Run tests automatically every day at 2 AM (without pushing code):**

1. Go to **Code** tab
2. Find and open `.github/workflows/docker-ci.yml`
3. Click pencil ✏️ to edit
4. Find the `on:` section (top of file):
   ```yaml
   on:
     pull_request:
     push:
       branches:
         - main
   ```

5. Add a schedule:
   ```yaml
   on:
     pull_request:
     push:
       branches:
         - main
     schedule:
       - cron: '0 2 * * *'  # Every day at 2 AM UTC
   ```

6. Commit with message: "Add scheduled tests"

7. Now tests run automatically every day!

---

## Part J: Viewing Secrets (But Not the Values!)

**GitHub lets you see secret names, but never shows the actual values (for security).**

### To verify your secrets exist:

1. Go to **Settings** > **Secrets and variables** > **Actions**

2. You see a list:
   ```
   ✅ OPENAI_API_KEY    (Updated 1 hour ago)
   ✅ PINECONE_API_KEY  (Updated 1 hour ago)
   ```

3. Click a secret to edit it
   ```
   Name: OPENAI_API_KEY
   Secret: [UPDATE BUTTON] [REMOVE BUTTON]
   ```

4. To **update a secret:**
   - Click the secret
   - Click **"Update secret"**
   - Paste new value
   - Click **"Update secret"**

5. To **remove a secret:**
   - Click the secret
   - Click **"Remove"** button
   - Confirm

---

## Part K: Complete Web Workflow (Summary)

**Everything you need to do from GitHub.com:**

```
1. Get API keys
   ├─ OpenAI: https://platform.openai.com/api-keys
   └─ Pinecone: https://app.pinecone.io

2. Add to GitHub
   ├─ Your repo > Settings > Secrets and variables > Actions
   ├─ New secret: OPENAI_API_KEY
   └─ New secret: PINECONE_API_KEY

3. Make a change
   ├─ Your repo > Code > Edit a file (click ✏️)
   ├─ Make change
   └─ Commit directly to main

4. Watch tests run
   ├─ Your repo > Actions tab
   ├─ See workflow running
   └─ Click to see details

5. All done! ✅
   └─ Every future push triggers tests automatically
```

---

## Part L: GitHub Actions Status Indicators

**What each icon means:**

| Icon | Meaning | What It Means |
|------|---------|--------------|
| 🟡 | In Progress | Tests are currently running |
| 🟢 ✅ | Success | All tests passed! Great job! |
| 🔴 ❌ | Failed | Something went wrong (see logs) |
| ⏭️ | Skipped | Step was skipped (usually needs secrets) |
| ⭕ | Pending | Waiting to start |
| ⏸️ | Cancelled | You cancelled it manually |

---

## Part M: Real-World Scenarios

### Scenario 1: You Updated a Chunk File

```
1. You open README.md or any chunk file
2. Click pencil ✏️ to edit
3. Make changes
4. Commit with message "Updated chunk"
5. Go to Actions tab
6. See "Docker CI" workflow running
7. Tests verify your change is valid
8. ✅ All pass = your change is safe!
9. ❌ Any fail = you need to fix something
```

### Scenario 2: You Added New Code

```
1. You edit atlas_engine/chat.py (from web editor)
2. Commit changes
3. Go to Actions tab
4. Watch Docker build
5. If build fails, click error to see why
6. Fix the error and commit again
7. Repeat until ✅ all tests pass
```

### Scenario 3: You Want to Test Before Committing

```
1. Don't commit yet
2. Go to Actions tab
3. Click "Docker CI" workflow
4. Click "Run workflow" button
5. Tests run with current code
6. If they pass, commit safely
7. If they fail, fix in web editor and try again
```

---

## Part N: Watching Tests in Real-Time

**GitHub Actions shows live progress (updates every few seconds):**

1. Go to **Actions** tab
2. Click the active workflow run
3. You see jobs starting:
   ```
   build-and-smoke-test    In progress... 2m 15s ⏳
   ```

4. Click the job to expand it
5. Watch steps complete in real-time:
   ```
   ✅ Checkout                   0.2s
   ✅ Set up Docker Buildx       1.5s
   🟡 Build image (CI)           In progress... 3m 45s ⏳
   ```

6. As you watch, the time increases automatically

7. When a step finishes, it gets a checkmark:
   ```
   ✅ Build image (CI)           4m 20s
   ```

8. Next step automatically starts

9. When everything finishes, you see all green:
   ```
   ✅ build-and-smoke-test       4m 30s
   ✅ Atlas integration flow     1m 20s
   ✅ publish-ghcr               2m 40s
   ```

---

## Part O: Troubleshooting from Web

### Problem: Can't Find Secrets Section

**Solution:**
1. Go to your repo
2. Click **Settings** (gear icon)
3. Click **Code and automation** section (left sidebar)
4. Click **Secrets and variables**
5. Click **Actions**

---

### Problem: Forgot Your API Key Value

**Solution:**
- You can't recover a secret's value (GitHub doesn't show it)
- But you can **update** it:
  1. Go to Settings > Secrets > Actions
  2. Click the secret
  3. Click **"Update secret"**
  4. Paste new value

---

### Problem: Tests Pass Locally But Fail on GitHub

**Solution:**
1. Check your secrets are correct (Settings > Secrets)
2. Check you committed all necessary files
3. Check `.env` directory is in `.gitignore` (so keys not committed)
4. Try running workflow manually (Actions > Run workflow button)

---

## ✅ Quick Checklist (Web Only)

- [ ] Got OpenAI API key from https://platform.openai.com/api-keys
- [ ] Got Pinecone API key from https://app.pinecone.io
- [ ] Added OPENAI_API_KEY secret in GitHub
- [ ] Added PINECONE_API_KEY secret in GitHub
- [ ] Made a change to your repo (or ran workflow manually)
- [ ] Went to Actions tab
- [ ] Saw workflow running (yellow 🟡)
- [ ] Watched it complete (green ✅)
- [ ] Clicked to see test details
- [ ] All 7 steps passed: [1/7], [2/7], ... [7/7]

**If all checked: You're done! 🎉**

---

## 🎓 What You Learned

✅ What GitHub Actions is (automation in the cloud)
✅ How to add API keys safely (GitHub Secrets)
✅ How to make changes (web editor)
✅ How to commit (web interface)
✅ How to watch tests run (Actions tab)
✅ How to troubleshoot (read logs)
✅ How to understand results (icons and colors)
✅ How to manually trigger tests (Run workflow button)

**Everything without opening a terminal!** 🚀

---

**Next:** Read `GITHUB_ACTIONS_SETUP.md` for complete details and command-line options.

**Need help?** Check the Troubleshooting sections above!

---

**Last updated:** February 2026
**Atlas Engine Version:** 2.0+
