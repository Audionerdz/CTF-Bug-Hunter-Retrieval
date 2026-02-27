# Docker Troubleshooting

**Specific errors and fixes for Docker-related issues.**

---

## Installation

### "docker: command not found"

**Solution:**

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Verify
docker --version
```

### "Got permission denied"

**Solution:**

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply group changes
newgrp docker

# Or logout and login again

# Verify
docker ps
```

---

## Building Images

### "No space left on device"

**Cause:** Disk full

**Solution:**

```bash
# Check disk
df -h

# Clean up
docker system prune -a --volumes

# Or manually
rm -rf ~/.docker/containers/*
rm -rf ~/.docker/images/*
```

### "Build context too large"

**Cause:** .dockerignore not excluding files

**Solution:**

```bash
# Verify .dockerignore exists
cat .dockerignore

# Should exclude:
# venv
# .git
# __pycache__
# .env
# chat_history

# Rebuild
docker build -t atlas-engine:local .
```

### "Failed to build: ModuleNotFoundError"

**Cause:** Dependency missing in requirements.txt

**Solution:**

```bash
# Check requirements.txt
cat requirements.txt

# If missing, add:
echo "langchain>=0.3.0" >> requirements.txt

# Rebuild
docker build -t atlas-engine:local .
```

---

## Running Containers

### "Error response from daemon: Cannot find image"

**Cause:** Image doesn't exist

**Solution:**

```bash
# Build image first
docker build -t atlas-engine:local .

# Or load from tar
docker load -i atlas-engine.tar.gz

# Verify
docker images
```

### "Bind for 0.0.0.0:8000 failed: address already in use"

**Cause:** Port already taken

**Solution:**

```bash
# Find process using port
lsof -i :8000
# or
netstat -tulnp | grep 8000

# Kill process
kill -9 <PID>

# Or use different port
docker run -p 9000:8000 ...
```

### "Container exited with code 1"

**Cause:** Error in entrypoint script

**Solution:**

```bash
# See logs
docker logs <container_id>

# Run with different command
docker run -it atlas-engine:local /bin/bash

# Debug manually
python3 -c "from atlas_engine import Atlas; Atlas()"
```

---

## Volume Mounting

### "Error: Permission denied reading .env files"

**Cause:** Volume permissions issue

**Solution:**

```bash
# Fix .env permissions
chmod 644 ~/.env/*.env
chmod 755 ~/.env

# Or run with correct user
docker run -u $(id -u):$(id -g) \
  -v ~/.env:/app/.env:ro \
  atlas-engine:local src/gemini_rag.py
```

### "Cannot access mounted volume"

**Cause:** Mount path doesn't exist or permission denied

**Solution:**

```bash
# Verify path exists
ls -la ~/.env/

# Use absolute path
docker run -v "$(pwd)/.env:/app/.env:ro" ...

# Check Docker can access volume
docker run -v ~/.env:/app/test:ro \
  atlas-engine:local ls -la /app/test
```

---

## Saving/Loading Images

### "Failed to save image: write error"

**Cause:** Disk full or permission denied

**Solution:**

```bash
# Check space
df -h

# Check permissions
touch /tmp/test.tar

# Save to different location
docker save atlas-engine:prod -o /tmp/atlas-engine.tar.gz
```

### "docker load: invalid tar format"

**Cause:** Tar file corrupted or truncated

**Solution:**

```bash
# Verify file
tar -tzf atlas-engine.tar.gz | head

# If corrupted, re-export from source
docker save atlas-engine:prod -o atlas-engine.tar.gz

# Check size (should be ~567MB)
ls -lh atlas-engine.tar.gz
```

### "Image load succeeded but cannot run"

**Cause:** Tar load incomplete

**Solution:**

```bash
# Re-load
docker load -i atlas-engine.tar.gz

# Or verify integrity
docker images | grep atlas

# If missing, re-export
```

---

## Networking

### "Failed to resolve image registry"

**Cause:** No internet or DNS issue

**Solution:**

```bash
# Check internet
ping 8.8.8.8

# Check DNS
nslookup docker.io

# Check Docker daemon
docker ps
```

### "Cannot connect to Ollama (port 11434)"

**Cause:** Ollama not running or not accessible

**Solution:**

```bash
# Start Ollama
ollama serve

# If in container, expose network
docker run --network=host atlas-engine:local ...

# Or map port
docker run -p 11434:11434 \
  -e OLLAMA_BASE_URL=http://localhost:11434 \
  atlas-engine:local src/gemini_rag.py --backend ollama
```

---

## Cleanup

### "Too many dangling images"

**Solution:**

```bash
# Remove unused containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Nuclear option (remove everything)
docker system prune -a --volumes
```

### "Image takes too much space"

**Solution:**

```bash
# Check sizes
docker images --format "{{.Repository}}:{{.Tag}}\t{{.Size}}"

# Remove old versions
docker rmi atlas-engine:old-version

# Or rebuild without cache
docker build --no-cache -t atlas-engine:local .
```

---

## Performance

### "Container runs slow"

**Solution:**

```bash
# Check resources
docker stats <container_id>

# Limit CPU
docker run --cpus="2" atlas-engine:local ...

# Limit memory
docker run --memory="2g" atlas-engine:local ...

# Check disk I/O
docker stats --no-stream
```

### "Container killed (OOMKilled)"

**Cause:** Out of memory

**Solution:**

```bash
# Increase memory
docker run --memory="4g" atlas-engine:local ...

# Or on Docker Desktop:
# Docker icon > Preferences > Resources > Memory > Set to 4GB+

# Check usage
docker stats
```

---

## Debugging

### Get container shell

```bash
# Run interactive
docker run -it atlas-engine:local /bin/bash

# Or exec into running
docker exec -it <container_id> /bin/bash
```

### View logs

```bash
# All logs
docker logs <container_id>

# Last 20 lines
docker logs --tail 20 <container_id>

# Follow logs
docker logs -f <container_id>

# With timestamps
docker logs -t <container_id>
```

### Inspect container

```bash
# Full config
docker inspect <container_id>

# Image details
docker inspect <image_id>

# Network
docker network inspect bridge
```

---

## Transfer Issues

### "SCP transfer hangs"

**Cause:** Network or large file

**Solution:**

```bash
# Check progress
# Let it finish (567MB at 1 Mbps = ~50 minutes)

# Or use faster method
rsync -avz atlas-engine.tar.gz user@host:/tmp/

# Or compress more
gzip -9 atlas-engine.tar.gz
```

### "Cannot transfer to home lab"

**Cause:** Network/SSH issue

**Solution:**

```bash
# Test SSH first
ssh user@192.168.1.50 "echo ok"

# If fails, check:
# - IP address correct?
# - User credentials correct?
# - Firewall allowing SSH?

# Debug SCP
scp -vv atlas-engine.tar.gz user@192.168.1.50:/tmp/
```

---

## Docker Compose

### "docker-compose: command not found"

**Solution:**

```bash
# Install Docker Compose
sudo apt-get install docker-compose

# Or use docker compose (v2)
docker compose up
```

### "Cannot start service: port already allocated"

**Solution:**

```bash
# Stop existing container
docker-compose down

# Or change port in docker-compose.yml
# ports:
#   - "9000:8000"  # Changed from 8000:8000
```

---

## Still Broken?

**Check in this order:**

1. Docker installed? `docker --version`
2. Docker running? `docker ps`
3. Image built? `docker images`
4. Permissions OK? `docker run --rm hello-world`
5. Volume mounted correctly? `docker run -v $PWD:/test ls -la /test`
6. File exists in context? `ls -la file` before `docker build`

---

**Last updated:** February 2026
**Atlas Engine Version:** 2.0+
