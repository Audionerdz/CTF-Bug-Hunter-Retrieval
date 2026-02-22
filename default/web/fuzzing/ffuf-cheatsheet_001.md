---
chunk_id: technique::web::fuzzing::ffuf-cheatsheet::001
domain: web
chunk_type: reference
confidence: 5
reuse_level: 1
tags: [ffuf, web-security, fuzzing, enumeration, htb-academy, seclists]
---

# Guía Maestra de Fuzzing Web con ffuf

Esta guía recopila los comandos esenciales para el descubrimiento de activos web utilizando `ffuf` (Fuzz Faster U Fool), categorizados por fase de auditoría.



## 1. Comandos de Descubrimiento de Contenido y Estructura

### Fuzzing de Directorios y Páginas
- **Directorios**: `ffuf -w wordlist.txt:FUZZ -u http://SERVER_IP:PORT/FUZZ`
- **Extensiones**: `ffuf -w wordlist.txt:FUZZ -u http://SERVER_IP:PORT/indexFUZZ`
- **Páginas Específicas**: `ffuf -w wordlist.txt:FUZZ -u http://SERVER_IP:PORT/blog/FUZZ.php`

### Fuzzing Recursivo (Profundidad)
Para buscar dentro de subdirectorios encontrados automáticamente:
- **Comando**: `ffuf -w wordlist.txt:FUZZ -u http://SERVER_IP:PORT/FUZZ -recursion -recursion-depth 1 -e .php -v`

## 2. Descubrimiento de Infraestructura y VHosts

### Subdominios y Virtual Hosts
- **Subdominios (DNS)**: `ffuf -w wordlist.txt:FUZZ -u https://FUZZ.hackthebox.eu/`
- **Virtual Hosts (HTTP Header)**: `ffuf -w wordlist.txt:FUZZ -u http://academy.htb:PORT/ -H 'Host: FUZZ.academy.htb' -fs [size]`

> [!IMPORTANT]
> Para VHosts, es vital usar el filtro `-fs` (Filter Size) para ignorar el tamaño de la respuesta por defecto del servidor.

## 3. Fuzzing de Parámetros y Valores (Explotación)

### Descubrimiento de Parámetros
- **GET**: `ffuf -w wordlist.txt:FUZZ -u "http://admin.academy.htb:PORT/admin/admin.php?FUZZ=key" -fs [size]`
- **POST**: `ffuf -w wordlist.txt:FUZZ -u http://admin.academy.htb:PORT/admin/admin.php -X POST -d 'FUZZ=key' -H 'Content-Type: application/x-www-form-urlencoded' -fs [size]`

### Descubrimiento de Valores
- **Comando**: `ffuf -w ids.txt:FUZZ -u http://admin.academy.htb:PORT/admin/admin.php -X POST -d 'id=FUZZ' -H 'Content-Type: application/x-www-form-urlencoded' -fs [size]`

## 4. Diccionarios Recomendados (SecLists)
- **Web Content**: `/opt/useful/seclists/Discovery/Web-Content/directory-list-2.3-small.txt`
- **Extensiones**: `/opt/useful/seclists/Discovery/Web-Content/web-extensions.txt`
- **DNS/Subdominios**: `/opt/useful/seclists/Discovery/DNS/subdomains-top1million-5000.txt`
- **Parámetros**: `/opt/useful/seclists/Discovery/Web-Content/burp-parameter-names.txt`

## 5. Utilidades y Comandos Misceláneos

### Preparación del Entorno
- **Añadir DNS local**: `sudo sh -c 'echo "SERVER_IP academy.htb" >> /etc/hosts'`
- **Generar lista numérica**: `for i in $(seq 1 1000); do echo $i >> ids.txt; done`

### Validación Manual
- **Petición POST con curl**: `curl http://admin.academy.htb:PORT/admin/admin.php -X POST -d 'id=key' -H 'Content-Type: application/x-www-form-urlencoded'`

---
