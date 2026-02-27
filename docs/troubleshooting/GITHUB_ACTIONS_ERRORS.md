# GitHub Actions Troubleshooting

**Specific errors and fixes for GitHub Actions workflows.**

---

## Workflow Not Running

### "No workflows found"

**Cause:** `.github/workflows/docker-ci.yml` not in repository

**Solution:**

```bash
# Check file exists
ls -la .github/workflows/docker-ci.yml

# If missing, copy it
cp docker-ci.yml .github/workflows/

# Push to GitHub
git add .github/workflows/
git commit -m "Add GitHub Actions workflow"
git push origin main
```

### "Workflow disabled"

**Cause:** Workflow was manually disabled

**Solution:**

1. Go to GitHub.com > Your Repo > Actions
2. Click **All workflows** (left sidebar)
3. Find **Docker CI**
4. Click three dots (...) > Enable workflow

---

## Workflow Fails at Build

### "Docker build failed: No such file"

**Cause:** Missing file in build context

**Solution:**

```bash
# Check file exists locally
ls -la src/ci_integration.py
ls -la Dockerfile

# If missing, add it
git add src/ci_integration.py Dockerfile
git commit -m "Add missing files"
git push origin main
```

### "Failed to fetch base image"

**Cause:** Can't download Python base image

**Solution:**

```bash
# Usually temporary. Retry by:
# Go to Actions > Docker CI > Run workflow > Run workflow
```

### "Build exceeded time limit"

**Cause:** Too slow (>6 hours)

**Solution:**

```bash
# Unlikely unless building in poor conditions
# Try again, or check network
```

---

## Smoke Test Fails

### "smoke-ok not found"

**Cause:** Atlas import failed in container

**Solution:**

1. Test locally:
   ```bash
   docker build -t atlas-engine:local .
   docker run --rm atlas-engine:local python3 -c "from atlas_engine import Atlas; print('ok')"
   ```

2. If fails locally, fix error and commit:
   ```bash
   git add .
   git commit -m "Fix import error"
   git push origin main
   ```

---

## Integration Test Fails

### "Integration test skipped (SKIPPED)"

**Cause:** API keys not added to GitHub Secrets

**Solution:**

1. Go to GitHub.com > Your Repo > Settings
2. Click **Secrets and variables** > **Actions**
3. Add `OPENAI_API_KEY` secret
4. Add `PINECONE_API_KEY` secret
5. Trigger workflow again: Actions > Docker CI > Run workflow

### "[1/7] ask(gpt) failed: API key invalid"

**Cause:** API key is wrong

**Solution:**

1. Go to Settings > Secrets
2. Delete `OPENAI_API_KEY`
3. Click **New repository secret**
4. Paste correct key
5. Run workflow again

### "[2/7] query: No results found"

**Cause:** Pinecone index or namespace issue

**Solution:**

1. Check index exists: https://app.pinecone.io
2. Check default namespace has data:
   ```bash
   # Locally:
   from atlas_engine import Atlas
   a = Atlas()
   results = a.query("test")
   print(len(results))  # Should be > 0
   ```

### "[5/7] vectorize failed: Permission denied"

**Cause:** Cannot write to isolated namespace

**Solution:**

```bash
# Check Pinecone API key has write permissions
# Usually not an issue. Try again with:

# Actions > Docker CI > Run workflow > Run workflow
```

### "[6/7] delete failed: Chunk not found"

**Cause:** Chunk ID not in Pinecone

**Solution:**

```bash
# This is rare. Usually means:
# - Vectorize didn't complete
# - Pinecone lag (try again in 30 sec)
# - Run workflow again
```

---

## Publish to GHCR Fails

### "Failed to log in to GHCR"

**Cause:** GitHub token missing or invalid

**Solution:**

```bash
# Usually automatic. Check:
# Settings > Actions > General > Workflow permissions

# Should be: "Read and write permissions"
```

### "Image push failed"

**Cause:** Network or storage issue

**Solution:**

```bash
# Usually temporary. Retry:
# Actions > Docker CI > Run workflow (on main)
```

---

## Logs & Debugging

### Where to find logs

1. Go to GitHub.com > Your Repo > **Actions** tab
2. Click the workflow run
3. Click the job (e.g., **build-and-smoke-test**)
4. Click step to expand and see output

### Common log locations

```
build-and-smoke-test
  ├─ Checkout
  ├─ Set up Docker Buildx
  ├─ Build image (CI)          ← Docker logs here
  ├─ Smoke test container      ← Import errors here
  ├─ Prepare CI env files
  └─ Atlas integration flow     ← Test errors here
```

### Export logs

1. Click **...** (top right of workflow)
2. Click **Download logs**
3. Unzip and read `.txt` files

---

## Secrets Issues

### "Secret name not recognized"

**Cause:** Secret name typo or missing

**Solution:**

```bash
# Check exact name in workflow:
# .github/workflows/docker-ci.yml

# Should reference:
# ${{ secrets.OPENAI_API_KEY }}
# ${{ secrets.PINECONE_API_KEY }}

# In Settings, exact names must match
```

### "Secret value is blank/empty"

**Cause:** Copied empty value

**Solution:**

1. Go to Settings > Secrets
2. Click the secret
3. Click **Update secret**
4. Paste the full value (check for leading/trailing spaces)
5. Click **Update secret**

---

## Rate Limiting

### "429 Too Many Requests"

**Cause:** Hit API rate limit

**Solution:**

```bash
# Wait 1 hour and try again
# Or upgrade API plan

# Check:
# - https://platform.openai.com/account/billing/overview (OpenAI)
# - https://app.pinecone.io (Pinecone)
```

---

## Network Issues (Self-Hosted Runners)

### "Network timeout in GitHub"

**Cause:** Runner can't reach APIs

**Solution:**

```bash
# If using self-hosted runner:
# - Check firewall rules
# - Check VPN/Proxy settings
# - Check DNS resolution

nslookup api.openai.com
curl https://api.openai.com/
```

---

## Re-Running Tests

### Manual retry

```bash
# Actions > Click workflow run > Re-run > Re-run all jobs
```

### Trigger workflow without push

```bash
# Actions > Docker CI > Run workflow > Run workflow
```

---

## Still Failing?

**Check in this order:**

1. API keys correct? (Settings > Secrets)
2. Workflow file valid? (`.github/workflows/docker-ci.yml`)
3. Tests pass locally?
   ```bash
   docker build -t atlas-engine:local .
   docker run --rm -v ./.env:/app/.env:ro atlas-engine:local src/ci_integration.py
   ```
4. Recent changes to code that might break tests?
5. GitHub status page: https://www.githubstatus.com/

---

**Last updated:** February 2026
**Atlas Engine Version:** 2.0+
