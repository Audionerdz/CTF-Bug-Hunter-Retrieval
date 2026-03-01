---
chunk_id: technique::web::vulnerability-scanning::ssti::scanner::tinja-ssti::001
domain: web
chunk_type: technique
confidence: 5
reuse_level: 1
tags: [tinja, ssti, template-injection, vulnerability-scanning, web-security]
---

# Detección de SSTI mediante el uso de TInjA

TInjA es una herramienta especializada en la detección de inyecciones de plantillas en el lado del servidor (SSTI). Automatiza el envío de múltiples payloads políglotas para identificar qué motor de renderizado (Jinja2, Mako, Twig, etc.) está procesando la entrada.



## 1. Modos de Operación y Comandos Esenciales

TInjA permite auditar desde parámetros simples hasta peticiones HTTP complejas extraídas de archivos.

### Auditoría de URL Única (GET/POST)
- **Escaneo básico**: `tinja url -u "http://TARGET/path?param=val"`
- **Inyección manual de prueba**: `tinja url -u "http://TARGET/vuln?name={{7*7}}"`
- **Envío de datos POST**: `tinja url -u "http://TARGET/login" --data "user=admin&pass={{7*7}}"`
- **Uso de Proxy (Análisis en Burp)**: `tinja url -u "http://TARGET" --proxy http://127.0.0.1:8080`

### Auditoría Avanzada
- **Desde petición Raw**: `tinja raw -r request.txt` (Ideal para peticiones con múltiples headers o estructuras complejas).
- **Modo Batch (Múltiples objetivos)**: `tinja bulk -l targets.txt`

## 2. Flujo de Trabajo Recomendado

Para una detección efectiva de SSTI, se debe seguir un proceso lógico que minimice el ruido y maximice la precisión.

1.  **Reconocimiento**: Identificar puntos donde la entrada del usuario se refleja en la respuesta (Parámetros, Cookies, Headers).
2.  **Confirmación**: Inyectar payloads aritméticos inofensivos (ej. `{{7*7}}`) y verificar si el servidor devuelve el resultado calculado (`49`).
3.  **Identificación**: Utilizar TInjA para determinar el motor específico mediante el análisis de errores y comportamientos de payloads específicos de lenguaje.
4.  **Extracción/Reporte**: Exportar los hallazgos en formato JSON para su posterior análisis o integración en reportes.



## 3. Flags y Parámetros de Control

Optimiza el escaneo según la infraestructura objetivo:

- **--timeout [seg]**: Ajusta el tiempo de espera (útil en redes lentas).
- **--threads [n]**: Controla la concurrencia del escaneo.
- **--no-follow**: Evita que la herramienta siga redirecciones HTTP (3xx), manteniendo el foco en el endpoint original.
- **-o json**: Genera la salida en formato JSON, ideal para procesar con `jq`.

## 4. Snippet para Documentación (Obsidian)

Para mantener un registro rápido de la prueba realizada:

```bash
tinja url -u "http://IP:PORT/search?q=test" --proxy [http://127.0.0.1:8080](http://127.0.0.1:8080) -o json > scan_results.json
