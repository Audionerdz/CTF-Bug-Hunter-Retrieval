---
chunk_id: technique::network::enumeration::directory-fuzzing::001
domain: network
chunk_type: technique
confidence: 5
reuse_level: 1
tags: [ffuf, directory-bruteforce, web-recon, fuzzing, seclists, enumeration]
---

# Descubrimiento de directorios web mediante Fuzzing con ffuf

El fuzzing de directorios es una técnica de descubrimiento de contenido que consiste en realizar peticiones HTTP sistemáticas contra un servidor web utilizando un diccionario de nombres comunes. El objetivo es identificar rutas ocultas que no están vinculadas directamente en la interfaz del sitio.

## 1. Configuración del Comando ffuf
Para ejecutar el descubrimiento, se debe definir la fuente de datos (wordlist) y el punto de inyección en la URL mediante el marcador `FUZZ`.

### Estructura base:
```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ \
-u "http://target.htb/FUZZ"
```

**Parámetros principales:**
- `-w`: Especifica el wordlist (diccionario de nombres)
- `-u`: URL objetivo donde se inyecta FUZZ
- `-FUZZ`: Marcador que será reemplazado por cada línea del wordlist

## 2. Ejecución con Filtrado
Para reducir ruido, es común filtrar respuestas por código de estado o tamaño:

```bash
# Filtrar códigos 404 y 403
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ \
-u "http://target.htb/FUZZ" \
-fc 404,403

# Filtrar por tamaño (size)
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ \
-u "http://target.htb/FUZZ" \
-fs 1234
```

**Opciones útiles:**
- `-fc [códigos]`: Filter Code - ignora respuestas con estos códigos HTTP
- `-fs [tamaño]`: Filter Size - ignora respuestas de este tamaño
- `-fw [palabras]`: Filter Words - ignora respuestas con este número de palabras

## 3. Interpretación de Resultados
Los resultados mostrados incluyen:
- **URL**: Ruta descubierta
- **Status**: Código HTTP (200, 301, 403, etc.)
- **Size**: Tamaño de la respuesta en bytes

Códigos de interés:
- `200`: Directorio/archivo accesible
- `301/302`: Redirección (posible directorio con trailing slash)
- `403`: Acceso denegado (pero existe)
- `404`: No encontrado (filtrar estos)
