# GitHub Actions Quick Start (5 Minutes)

**The absolute fastest way to get Atlas running on GitHub Actions.**

---

## 🎯 Your Goal

After 5 minutes, you'll have:
- ✅ API keys stored safely in GitHub
- ✅ Automated tests running when you push code
- ✅ Docker image building automatically
- ✅ Full integration tests validating your app

---

## ⏱️ Step 1: Add API Keys (2 minutes)

### On GitHub.com

1. **Open your repository**
   ```
   https://github.com/YOUR-USERNAME/YOUR-REPO
   ```

2. **Go to Settings**
   ```
   Click: Settings (gear icon, top right)
   ```

3. **Go to Secrets**
   ```
   Left sidebar → Secrets and variables → Actions
   ```

4. **Add First Secret: OPENAI_API_KEY**
   ```
   Click: "New repository secret" (green button)
   
   Name: OPENAI_API_KEY
   Secret: (paste your OpenAI key from https://platform.openai.com/api-keys)
   
   Click: "Add secret"
   ```

5. **Add Second Secret: PINECONE_API_KEY**
   ```
   Click: "New repository secret" again
   
   Name: PINECONE_API_KEY
   Secret: (paste your Pinecone key)
   
   Click: "Add secret"
   ```

**Done!** Both secrets are now in GitHub (hidden from view).

---

## ⏱️ Step 2: Make a Change & Push (2 minutes)

### On Your Computer

```bash
# Go to your repo
cd /home/kali/Desktop/RAG

# Make a small change (any file)
echo "# Updated" >> README.md

# Commit and push
git add README.md
git commit -m "Update README"
git push origin main
```

**What happens next:** GitHub automatically starts tests!

---

## ⏱️ Step 3: Watch Tests Run (1 minute)

### On GitHub.com

1. **Go to Actions tab**
   ```
   Your repo → Click "Actions" tab (top)
   ```

2. **See your workflow running**
   ```
   "Docker CI" workflow should be running (yellow 🟡)
   ```

3. **Wait for it to finish**
   ```
   - 🟡 Yellow = Running
   - 🟢 Green = Success!
   - 🔴 Red = Failed
   ```

4. **Click on the workflow to see details**
   ```
   Click: "Docker CI" workflow run
   ```

5. **See all the steps**
   ```
   ✅ build-and-smoke-test
   ✅ Atlas integration flow (GPT + query + fetch + vectorize + delete)
   ✅ publish-ghcr (only on main)
   ```

---

## 🎉 That's It!

Your app is now **automatically tested** every time you push code.

---

## 📋 What Gets Tested?

Every time you push to `main`:

```
[STEP 1] Build Docker image
└─ Creates atlas-engine:ci container

[STEP 2] Smoke test
└─ Verifies Atlas imports correctly

[STEP 3] Integration tests (if you added API secrets)
├─ Ask GPT "What is LFI?" → ✅
├─ Query "ffuf cheatsheet" → ✅
├─ Ask GPT again (cache test) → ✅
├─ Fetch a chunk → ✅
├─ Vectorize test chunk → ✅
├─ Delete test chunk → ✅
└─ All data in isolated namespace (safe!)

[STEP 4] Push Docker image to GHCR
└─ Published at: ghcr.io/your-username/your-repo:latest
```

---

## 🚨 If Something Fails

### Failure: "Secrets are missing"

**You see:** "Integration flow (SKIPPED)"

**Fix:** Add `OPENAI_API_KEY` and `PINECONE_API_KEY` secrets (Step 1)

---

### Failure: "API error"

**You see:** "Failed at step [X/7]"

**Fix:**
1. Check your API key is correct
2. Check you have credit/quota left
3. Update the secret in GitHub
4. Push a new commit to re-run tests

---

### Failure: "Docker build failed"

**Fix:**
1. Test locally first:
   ```bash
   docker build -t atlas-engine:local .
   ```
2. Fix the error
3. Commit and push
4. Tests will automatically re-run

---

## 🔧 Advanced: Run Tests Anytime (Without Pushing Code)

### From GitHub Web

1. Go to **Actions** tab
2. Click **Docker CI** (left sidebar)
3. Click **Run workflow** (blue button)
4. Click **Run workflow** again (in the popup)
5. Tests start immediately!

---

## 🖥️ Advanced: Run Tests Locally First

**Before pushing, test locally to catch errors early:**

```bash
# 1. Navigate to your repo
cd /home/kali/Desktop/RAG

# 2. Build Docker image
docker build -t atlas-engine:local .

# 3. Run the integration tests
docker run --rm \
  -e ATLAS_CI_NAMESPACE="ci-local-test" \
  -v "/home/kali/Desktop/RAG/.env:/app/.env:ro" \
  atlas-engine:local src/ci_integration.py
```

**You'll see:**
```
[1/7] ask(gpt): What is LFI? ✅
[2/7] query: ffuf cheatsheet ✅
[3/7] ask(gpt) again: What is LFI? ✅
[4/7] fetch existing chunk ✅
[5/7] create + vectorize test chunk ✅
[6/7] delete test chunk ✅
[7/7] done ✅
```

**If this works locally, it will work on GitHub too!**

---

## 📊 Check Test Results from Command Line

```bash
# See last 5 workflow runs
gh run list --limit 5

# See details of the last run
gh run view

# See full logs of last run
gh run view --log

# Watch a specific run (live)
gh run view <run-id> --log --exit-status
```

---

## 🔒 Safety Guarantees

✅ **Your production data is safe:**
- All test writes go to `ci-{run_id}` namespace
- Test data is automatically deleted
- Your `__default__` namespace (production) never touched

✅ **Your API keys are safe:**
- Stored as GitHub Secrets (encrypted)
- Never printed in logs
- Never visible in code

✅ **Your code is safe:**
- Tests must pass before you deploy
- Failures show clearly
- You control when to push to main

---

## 📚 Next Steps

1. **Read the full guide:** `GITHUB_ACTIONS_SETUP.md`
2. **Understand each test:** See "What Each Test Does" section
3. **Learn troubleshooting:** See "Troubleshooting" section
4. **Customize workflow:** Edit `.github/workflows/docker-ci.yml`

---

## 🎓 Key Concepts Explained

| Term | What It Means |
|------|---------------|
| **Workflow** | A set of automated tasks that run in the cloud |
| **Job** | One of those tasks (e.g., "build-and-smoke-test") |
| **Step** | One action within a job (e.g., "Build image") |
| **Secret** | A hidden API key stored in GitHub (safe!) |
| **Namespace** | An isolated section of your Pinecone database |
| **Docker** | A container that includes all your code + dependencies |
| **GHCR** | GitHub Container Registry (free image hosting) |

---

## ✅ Checklist: Did You Complete Setup?

- [ ] Created GitHub account and pushed repo
- [ ] Added `OPENAI_API_KEY` secret
- [ ] Added `PINECONE_API_KEY` secret
- [ ] Made a commit and pushed to `main`
- [ ] Watched workflow run in Actions tab
- [ ] Saw all green checkmarks (✅)

**If all checked:** Congratulations! 🎉 Your Atlas app is now automated!

---

## 💬 Quick Questions

**Q: Will tests break my app if they fail?**
A: No. Tests run in isolation. Your app is safe.

**Q: Do I have to push to GitHub for tests to run?**
A: No. You can manually trigger tests from the Actions tab anytime.

**Q: Can I test locally before pushing?**
A: Yes! Run `docker build` and `docker run` first (recommended).

**Q: What if I want to skip tests for one commit?**
A: Don't commit to `main`. Use a feature branch and merge via Pull Request.

**Q: How much does this cost?**
A: GitHub Actions is free for public repos and 2000 minutes/month for private repos. Our tests take ~3 minutes each, so plenty of room!

---

## 📖 Full Documentation

For **complete details**, see: `GITHUB_ACTIONS_SETUP.md`

For **troubleshooting**, see: `GITHUB_ACTIONS_SETUP.md#troubleshooting`

---

**You're all set! 🚀**

Your Atlas app is now automated, tested, and safe.

Every commit → tests automatically run → you get instant feedback.

Enjoy!
