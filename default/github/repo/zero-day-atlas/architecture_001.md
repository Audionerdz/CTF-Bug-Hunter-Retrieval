---
chunk_id: reference::repo::zero-day-atlas::architecture::001
domain: GitHub 
chunk_type: reference
confidence: 5
reuse_level: 5
tags: [repo, arquitectura, zero-day-atlas, git, architecture, pentesting-workflow, documentation, repository-design]
---


# ZeroDays-Atlas: Arquitectura de Datos y Estándares de Operación

Una base de conocimientos de ciberseguridad requiere una arquitectura que permita la **búsqueda instantánea** y la **reproducibilidad de exploits**. Esta estructura está optimizada para ser indexada por motores RAG (Retrieval-Augmented Generation).



## 1. Desglose Estratégico de Directorios

### 📂 Web-Security (Lógica de Aplicación)
No solo contiene payloads, sino vectores de ataque categorizados por el impacto en el servidor o cliente.
- **Payloads.txt**: Listas crudas para intrusión rápida (LFI, XSS, SSRF).
- **Manual-Exploitation**: Notas sobre cómo bypassear WAFs o filtros específicos.

### 📂 Network-Exploitation (Táctica de Infraestructura)
Organizado por el **Protocolo**, facilitando la consulta durante un escaneo de Nmap.
- **Port-XX**: Cada puerto contiene comandos para:
    1. **Enumeración**: Scripts de Nmap y herramientas específicas (ej: `enum4linux`).
    2. **Fuerza Bruta**: Configuraciones recomendadas para Hydra o Medusa.
    3. **Exploits**: Enlaces a herramientas como Metasploit o scripts de GitHub.

### 📂 Exploits-CVE (Análisis de Vulnerabilidades)
Es el componente de investigación. Cada CVE debe contener:
- `Analysis.md`: Explicación técnica de la vulnerabilidad (Root Cause Analysis).
- `PoC.py/sh`: Código funcional para replicar el hallazgo en entornos controlados.
- `Dork.txt`: Consultas de Google o Shodan para identificar sistemas expuestos.

## 2. Convenciones de Nomenclatura (Naming Convention)
Para garantizar que el sistema sea profesional y fácil de automatizar:

* **Carpetas**: `Kebab-case` (ej: `Broken-Access-Control`).
* **Scripts**: `snake_case` (ej: `exploit_smb_v3.py`).
* **Writeups**: `YYYY-MM-DD-MachineName.md`.
* **Archivos de Datos**: `prefix-description.txt` (ej: `wordlist-common-paths.txt`).

## 3. Matriz de Relaciones del Repositorio

| Directorio | Relación Primaria | Herramienta Clave |
| :--- | :--- | :--- |
| `Network-Exploitation/` | Capa 3 y 4 del Modelo OSI | `nmap`, `impacket`, `netcat` |
| `Web-Security/` | Capa 7 (Aplicación) | `burp-suite`, `ffuf`, `sqlmap` |
| `Resources/` | Soporte transversal | `python`, `bash`, `sed/awk` |
| `Methodology/` | Estándar de cumplimiento | `PTES`, `OWASP-Testing-Guide` |



## 4. Optimización para Sistemas RAG
Para que tu bot de Telegram o IA encuentre información precisa:
- **Metadatos en archivos**: Cada archivo `.md` debe empezar con un encabezado YAML (como este chunk).
- **Archivos de Resumen**: Cada carpeta principal debe tener un `INDEX.md` que resuma su contenido.
- **Contexto**: Evita archivos vacíos; un `README.md` con dos líneas de contexto es mejor que solo una lista de archivos.

---

