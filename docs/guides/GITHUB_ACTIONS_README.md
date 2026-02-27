# GitHub Actions Documentation for Atlas Engine

**Welcome! This folder contains everything you need to automate your Atlas RAG application.**

---

## 📚 Documentation Index

Choose your learning style:

### 🚀 **Just Want to Get Started? (5 minutes)**
**→ Start here:** [`GITHUB_ACTIONS_QUICKSTART.md`](./GITHUB_ACTIONS_QUICKSTART.md)

- Super short version
- Get running in 5 minutes
- Perfect for beginners

---

### 🌐 **Using GitHub Web Interface Only? (No Terminal)**
**→ Start here:** [`GITHUB_ACTIONS_WEB_WALKTHROUGH.md`](./GITHUB_ACTIONS_WEB_WALKTHROUGH.md)

- Visual step-by-step guide
- Screenshots descriptions
- Everything explained
- Perfect for non-technical users

---

### 💻 **Prefer Command Line? (Terminal Only)**
**→ Start here:** [`GITHUB_ACTIONS_CLI.md`](./GITHUB_ACTIONS_CLI.md)

- Commands and aliases
- Shell scripts
- Monitoring workflows from terminal
- Perfect for developers

---

### 📖 **Want Complete Details? (Everything)**
**→ Start here:** [`GITHUB_ACTIONS_SETUP.md`](./GITHUB_ACTIONS_SETUP.md)

- Comprehensive guide
- All concepts explained
- Troubleshooting section
- Safety guarantees
- Advanced customization

---

## 🎯 Quick Navigation

| Need | Read | Time |
|------|------|------|
| **Get started ASAP** | `GITHUB_ACTIONS_QUICKSTART.md` | 5 min |
| **I'm using web only** | `GITHUB_ACTIONS_WEB_WALKTHROUGH.md` | 20 min |
| **I'm using terminal** | `GITHUB_ACTIONS_CLI.md` | 15 min |
| **Everything in detail** | `GITHUB_ACTIONS_SETUP.md` | 30 min |
| **One specific topic** | See index below | ⏱️ varies |

---

## 📋 Topics by Document

### GITHUB_ACTIONS_QUICKSTART.md
- What is GitHub Actions? (2 min explanation)
- Get API keys (5 min)
- Add keys to GitHub (2 min)
- Make a change & push (2 min)
- Watch tests run (1 min)
- **Result: App is automated!**

### GITHUB_ACTIONS_WEB_WALKTHROUGH.md
- Part A: Get API keys
- Part B: Add keys to GitHub (with detailed web steps)
- Part C: Make a change (3 methods)
- Part D: Watch tests automatically
- Part E: Understand the workflow timeline
- Part F: View test results in detail
- Part G: Fix common issues from web
- Part H: Manual trigger (run anytime)
- Part I: Scheduled tests
- Part J: Viewing secrets
- Part K: Complete web workflow summary
- Part L: Status indicators explained
- Part M: Real-world scenarios
- Part N: Watch tests in real-time

### GITHUB_ACTIONS_CLI.md
- Installation (GitHub CLI)
- Step 1: Add secrets via command line
- Step 2: Make changes & push
- Step 3: Watch tests run
- Step 4: See full logs
- Step 5: Trigger manually
- Advanced: Check specific jobs
- Troubleshooting from terminal
- Test locally before pushing
- Useful aliases for shortcuts
- Quick reference table
- Typical day workflow

### GITHUB_ACTIONS_SETUP.md
- What is GitHub Actions?
- Prerequisites
- Step 1: Add API keys (detailed)
- Step 2: Understanding the workflow
- Step 3: Running tests from web
- Step 4: Running tests from CLI
- What each test does (detailed breakdown)
- Troubleshooting (comprehensive)
- Safety first (guarantees & best practices)
- Typical workflows (step-by-step)
- Monitoring tests
- Advanced customization
- Quick reference cheatsheet
- Summary

---

## 🚀 Start Here (Choose Your Path)

### Path 1: "I'm a total beginner and just want it working"
```
1. Read: GITHUB_ACTIONS_QUICKSTART.md (5 min)
2. Follow the steps exactly
3. Done!
```

### Path 2: "I only use the web browser"
```
1. Read: GITHUB_ACTIONS_WEB_WALKTHROUGH.md (20 min)
2. Follow the detailed web steps
3. Everything explained
4. Done!
```

### Path 3: "I'm comfortable with terminal"
```
1. Read: GITHUB_ACTIONS_CLI.md (15 min)
2. Use the commands provided
3. Customize with aliases
4. Done!
```

### Path 4: "I want to understand everything"
```
1. Read: GITHUB_ACTIONS_SETUP.md (30 min)
2. All concepts explained
3. Learn why things work
4. Troubleshoot anything
5. Done!
```

---

## 🔑 Key Concepts (For All Paths)

**GitHub Actions:** Automated testing that runs when you push code to GitHub

**Secrets:** Hidden API keys stored safely in GitHub (never shown, never leaked)

**Workflow:** The set of instructions that runs automatically (build, test, deploy)

**Jobs:** Different parts of the workflow (build docker, run smoke test, run integration test)

**Namespace:** An isolated section of your Pinecone database used for testing (safe from production)

**Docker:** A container that includes all your code and dependencies

---

## ✅ What You'll Accomplish

After following any of these guides, you'll have:

- ✅ API keys stored securely in GitHub
- ✅ Automated tests running every time you push code
- ✅ Docker image building automatically
- ✅ Full integration tests validating:
  - `atlas.ask("What is LFI?", backend="gpt")`
  - `atlas.query("ffuf cheatsheet", top_k=3)`
  - `atlas.fetch("chunk_id")`
  - `atlas.vectorize(...)`
  - `atlas.delete(...)`
- ✅ Tests run in isolated namespace (your production data stays safe)
- ✅ Instant feedback when you break something
- ✅ Professional CI/CD pipeline

---

## 🛡️ Safety Guarantees

**Your app will NOT break:**
- Tests run in isolated namespace: `ci-{run_id}`
- Test data is deleted automatically
- Your production data (default namespace) never touched
- If tests fail, they don't stop your development
- You control when to deploy

---

## ⚠️ Before You Start

Make sure you have:
- [ ] GitHub account
- [ ] Your repository pushed to GitHub
- [ ] OpenAI API key (from https://platform.openai.com/api-keys)
- [ ] Pinecone API key (from https://app.pinecone.io)
- [ ] Admin access to your GitHub repo

---

## 🎯 Most Common Question: "Which guide should I read?"

**Answer: It depends on HOW you want to work:**

| How You Work | Read This | Time |
|--------------|-----------|------|
| I only use GitHub.com (web browser) | `GITHUB_ACTIONS_WEB_WALKTHROUGH.md` | 20 min |
| I use terminal and git commands | `GITHUB_ACTIONS_CLI.md` | 15 min |
| I want the fastest start possible | `GITHUB_ACTIONS_QUICKSTART.md` | 5 min |
| I want to understand EVERYTHING | `GITHUB_ACTIONS_SETUP.md` | 30 min |

---

## 🆘 Troubleshooting

### "I don't know which guide to read"
→ Start with `GITHUB_ACTIONS_QUICKSTART.md` (only 5 minutes)

### "I'm stuck on a step"
→ Look in the document's Troubleshooting section

### "I want to understand why something works"
→ Read `GITHUB_ACTIONS_SETUP.md` (explains concepts in detail)

### "I can't get tests running locally"
→ See `GITHUB_ACTIONS_SETUP.md` → "Docker (Recommended for CI/CD)"

### "Tests are failing in GitHub"
→ See your document's "Troubleshooting" section

---

## 📞 Questions?

If something isn't clear:
1. Re-read the relevant section
2. Check the Troubleshooting section
3. Check GitHub Actions docs: https://docs.github.com/en/actions

---

## 🎓 What You'll Learn

✅ What GitHub Actions is  
✅ How to store API keys safely  
✅ How to automate testing  
✅ How to use Docker in CI/CD  
✅ How to read test logs  
✅ How to troubleshoot failures  
✅ How to keep your app safe  

---

## 📊 Your Workflow After Setup

```
Every day, you:

1. Make changes to your code
   ↓
2. Commit & push to GitHub
   ↓
3. GitHub automatically runs tests
   ↓
4. You get instant feedback
   ├─ ✅ Green = Everything works!
   └─ ❌ Red = You broke something (fix it)
   ↓
5. Done!
```

---

## 🎉 Success Looks Like This

When everything is working:
- Every push triggers tests automatically
- Tests complete in ~9 minutes
- You see 3 green checkmarks (✅ build, ✅ smoke, ✅ integration)
- Your Docker image publishes to GHCR
- You sleep peacefully knowing your app is tested

---

## 📚 File Structure

```
Your Repository
├── .github/
│   └── workflows/
│       └── docker-ci.yml          ← The automation script
├── src/
│   └── ci_integration.py          ← Integration test script
├── Dockerfile                      ← Docker configuration
├── docker-compose.yml              ← Local docker setup
├── GITHUB_ACTIONS_README.md        ← You are here!
├── GITHUB_ACTIONS_QUICKSTART.md    ← 5-minute version
├── GITHUB_ACTIONS_WEB_WALKTHROUGH.md ← Web-only guide
├── GITHUB_ACTIONS_CLI.md           ← Terminal guide
└── GITHUB_ACTIONS_SETUP.md         ← Complete guide
```

---

## 🔗 External Links

- **OpenAI API Keys:** https://platform.openai.com/api-keys
- **Pinecone Console:** https://app.pinecone.io
- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **Docker Docs:** https://docs.docker.com/

---

## 📅 Last Updated

- **Date:** February 2026
- **Atlas Engine Version:** 2.0+
- **Documentation Version:** 1.0

---

## 🎯 Next Step

**Pick a guide above and start reading!**

- **5-minute version?** → `GITHUB_ACTIONS_QUICKSTART.md`
- **Web browser only?** → `GITHUB_ACTIONS_WEB_WALKTHROUGH.md`
- **Terminal commands?** → `GITHUB_ACTIONS_CLI.md`
- **Everything explained?** → `GITHUB_ACTIONS_SETUP.md`

---

**Good luck! You've got this! 🚀**
