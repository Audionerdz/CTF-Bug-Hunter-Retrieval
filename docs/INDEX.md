# Atlas Engine Documentation Index

**Organized guide to all Atlas documentation.**

---

## 📚 Quick Navigation

### 🚀 Getting Started (Choose Your Path)

- **[GitHub Actions Setup](./guides/GITHUB_ACTIONS_README.md)** - Automate with CI/CD
- **[Docker to Home Lab](./deployment/DOCKER_TO_HOME_LAB.md)** - Deploy to your VM
- **[Windows Setup](./guides/WINDOWS_SETUP.md)** - For Windows users

### 📖 Complete Guides (By Topic)

#### GitHub Actions (Automation)
- [Quick Start (5 min)](./guides/GITHUB_ACTIONS_QUICKSTART.md) - Fastest setup
- [Web Walkthrough](./guides/GITHUB_ACTIONS_WEB_WALKTHROUGH.md) - Browser-only (no terminal)
- [CLI Guide](./guides/GITHUB_ACTIONS_CLI.md) - Command line (for developers)
- [Complete Setup](./guides/GITHUB_ACTIONS_SETUP.md) - Full reference manual

#### Deployment
- [Docker to Home Lab](./deployment/DOCKER_TO_HOME_LAB.md) - VPS → Home VM (5 min)
  - Docker method
  - Python native method
  - Troubleshooting

#### Installation
- [Windows Setup](./guides/WINDOWS_SETUP.md) - Complete Windows guide

### 🛠️ Troubleshooting

- [Common Issues](./troubleshooting/COMMON_ISSUES.md)
- [GitHub Actions Errors](./troubleshooting/GITHUB_ACTIONS_ERRORS.md)
- [Docker Issues](./troubleshooting/DOCKER_ISSUES.md)

---

## 📊 Documentation by Use Case

### "I want to automate tests on GitHub"
1. Read: [GitHub Actions Quick Start](./guides/GITHUB_ACTIONS_QUICKSTART.md) (5 min)
2. Read: [GitHub Actions README](./guides/GITHUB_ACTIONS_README.md) (navigation)
3. Choose method:
   - Web only? → [Web Walkthrough](./guides/GITHUB_ACTIONS_WEB_WALKTHROUGH.md)
   - Terminal? → [CLI Guide](./guides/GITHUB_ACTIONS_CLI.md)
   - Want everything? → [Complete Setup](./guides/GITHUB_ACTIONS_SETUP.md)

### "I need to move Atlas to my home lab VM"
1. Read: [Docker to Home Lab](./deployment/DOCKER_TO_HOME_LAB.md) (5 min)
2. Choose method:
   - Docker? → Follow Docker section
   - Python? → Follow Python section
3. If issues → Check [Docker Issues](./troubleshooting/DOCKER_ISSUES.md)

### "I'm on Windows"
1. Read: [Windows Setup](./guides/WINDOWS_SETUP.md)
2. Follow step-by-step instructions
3. If errors → Check [Common Issues](./troubleshooting/COMMON_ISSUES.md)

### "Something broke!"
1. Check [Common Issues](./troubleshooting/COMMON_ISSUES.md)
2. If GitHub Actions → [GitHub Actions Errors](./troubleshooting/GITHUB_ACTIONS_ERRORS.md)
3. If Docker → [Docker Issues](./troubleshooting/DOCKER_ISSUES.md)

---

## 📋 File Organization

```
docs/
├── INDEX.md (you are here)
│
├── guides/
│   ├── GITHUB_ACTIONS_README.md          (Navigation for GitHub Actions)
│   ├── GITHUB_ACTIONS_QUICKSTART.md      (5-minute quick start)
│   ├── GITHUB_ACTIONS_WEB_WALKTHROUGH.md (Browser-only guide)
│   ├── GITHUB_ACTIONS_CLI.md             (Terminal guide)
│   ├── GITHUB_ACTIONS_SETUP.md           (Complete reference)
│   └── WINDOWS_SETUP.md                  (Windows installation)
│
├── deployment/
│   └── DOCKER_TO_HOME_LAB.md             (VPS → Home VM in 5 min)
│
└── troubleshooting/
    ├── COMMON_ISSUES.md                  (General problems)
    ├── GITHUB_ACTIONS_ERRORS.md          (CI/CD specific)
    └── DOCKER_ISSUES.md                  (Container specific)
```

---

## 🎯 Quick Links

| Need | Document | Time |
|------|----------|------|
| Fastest setup | [Quick Start](./guides/GITHUB_ACTIONS_QUICKSTART.md) | 5 min |
| Browser only | [Web Walkthrough](./guides/GITHUB_ACTIONS_WEB_WALKTHROUGH.md) | 20 min |
| Terminal | [CLI Guide](./guides/GITHUB_ACTIONS_CLI.md) | 15 min |
| Everything | [Complete Setup](./guides/GITHUB_ACTIONS_SETUP.md) | 30 min |
| Deploy to VM | [Docker Deploy](./deployment/DOCKER_TO_HOME_LAB.md) | 5 min |
| Windows | [Windows Setup](./guides/WINDOWS_SETUP.md) | 30 min |
| Fix something | [Troubleshooting](./troubleshooting/) | varies |

---

## 📚 Total Documentation

- **Total files:** 10 markdown guides
- **Total lines:** ~3,500+ lines of documentation
- **Coverage:** GitHub Actions, Docker, Deployment, Windows, Troubleshooting
- **For:** Total beginners to advanced developers

---

## 🚀 Start Here

1. **Not sure where to start?** → Read [INDEX.md](./INDEX.md) (this file)
2. **Want automation?** → [GitHub Actions Quick Start](./guides/GITHUB_ACTIONS_QUICKSTART.md)
3. **Need to deploy?** → [Docker to Home Lab](./deployment/DOCKER_TO_HOME_LAB.md)
4. **Something broken?** → [Troubleshooting](./troubleshooting/)

---

**Last updated:** February 2026
**Atlas Engine Version:** 2.0+
