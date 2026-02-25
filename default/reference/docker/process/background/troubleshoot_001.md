---
chunk_id: reference::docker::process::background::troubleshoot::001
domain: reference
chunk_type: technique
---

###  Background-Process

Ejecuta:

```bash
sudo netstat -tulpn | grep 8080
```

o, si no tienes `netstat`:

```bash
sudo lsof -i :8080
```

Verás algo como:

```
php     4532  ...  LISTEN  0.0.0.0:8080
```

o

```
docker-proxy 1234 ... 0.0.0.0:8080
```

### Paso 2 — Matar el proceso que usa ese puerto

Si, por ejemplo, el PID es `4532`, puedes detenerlo así:

```bash
sudo kill -9 4532
```

o si es otro contenedor de Docker:

```bash
docker ps | grep 8080
docker stop <container_id>
```
