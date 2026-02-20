---
chunk_id: technique::network::enumeration::subdomain-fuzzing::001
domain: network
chunk_type: technique
confidence: 5
reuse_level: 1
tags: [ffuf, dns, enumeration, seclists, subdomains]
---

# Enumeración de subdominios mediante Fuzzing con ffuf

La detección de subdominios se realiza mediante consultas a DNS públicos para verificar la existencia de registros asociados a un dominio principal. Esta técnica es esencial para expandir la superficie de ataque durante la fase de reconocimiento.

## 1. Requisitos Previos
Para ejecutar el ataque se requieren dos elementos fundamentales:
- **Diccionario (Wordlist):** Listado de nombres potenciales (Ej: `/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt`).
- **Dominio Objetivo:** La base sobre la cual se realizará la búsqueda (Ej: `wingdata.htb`).

## 2. Ejecución del Comando
El comando utiliza el placeholder `FUZZ` para inyectar cada palabra del diccionario en la estructura de la URL.

```bash
# Comando básico para fuzzing de subdominios
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ \
-u "http://FUZZ.wingdata.htb/"
```
