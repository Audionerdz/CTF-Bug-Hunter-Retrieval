---
chunk_id: procedure::web::web-enumeration::network-enumeration::001
domain: web
chunk_type: procedure
category: web-security
confidence: high
reuse_level: universal
tags: [enumeration, nmap, network, service-discovery, port-scanning]
source_file: /home/ftpuser/uploads/WINGDATA/Enumeracion WingData.md
---

## FASE 1: Enumeración y Descubrimiento

### 1.1 - Network Enumeration

**Objetivo**: Identificar servicios activos en la máquina

```bash
nmap -sV -sC 10.129.1.206
```

**Output esperado**:

```
Nmap scan report for 10.129.1.206
Host is up (0.0044s latency)

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Debian 3 (protocol 2.0)
80/tcp open  http    Apache httpd 2.4.66 ((Debian))
```

**Análisis**:

- SSH abierto en puerto 22 (posible vector de acceso si conseguimos credenciales)

- HTTP en puerto 80 (web application)
