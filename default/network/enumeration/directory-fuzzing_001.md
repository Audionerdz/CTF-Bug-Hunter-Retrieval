---
chunk_id: technique::network::enumeration::directory-fuzzing::001
domain: network
chunk_type: technique
---

# Descubrimiento de directorios web mediante Fuzzing con ffuf

El fuzzing de directorios es una técnica de descubrimiento de contenido que consiste en realizar peticiones HTTP sistemáticas contra un servidor web utilizando un diccionario de nombres comunes. El objetivo es identificar rutas ocultas que no están vinculadas directamente en la interfaz del sitio.



## 1. Configuración del Comando ffuf
Para ejecutar el descubrimiento, se debe definir la fuente de datos (wordlist) y el punto de inyección en la URL mediante el marcador `FUZZ`.

### Estructura base:
```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ \
-u "[http://target.htb/FUZZ"
```
