---
chunk_id: technique::network::enumeration::extension-fuzzing::001
domain: network
chunk_type: technique
---

# Identificación de extensiones y archivos mediante Fuzzing con ffuf

El fuzzing de extensiones permite determinar qué tecnología utiliza el servidor backend (PHP, ASP, HTML, etc.) identificando archivos base comunes con distintas terminaciones. Una vez identificado el lenguaje, se procede a buscar archivos específicos con esa extensión.



## 1. Identificación del Lenguaje del Servidor
Para descubrir la tecnología, se utiliza un nombre de archivo estándar (como `index`) y se fuzzear la extensión utilizando un diccionario especializado.

### Comando de descubrimiento de tecnología:
```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/web-extensions.txt:FUZZ \
-u "http://SERVER_IP:PORT/indexFUZZ"

```

**Interpretación de hallazgos:**

* **index.php (200 OK)**: Confirma que el servidor procesa archivos PHP.
* **index.phps (403 Forbidden)**: Indica que el recurso existe pero el acceso está restringido, reforzando la presencia de PHP.

## 2. Nombres de Archivos Críticos

Al buscar archivos, es recomendable priorizar nombres que suelen contener paneles de gestión o puntos de entrada:

* `index`, `login`, `admin`, `portal`, `dashboard`
* `home`, `default`, `main`, `user`, `panel`

## 3. Descubrimiento de Archivos Ocultos

Tras confirmar que el servidor usa PHP, se realiza un fuzzing de nombres de archivos dentro de directorios específicos (como `/blog/`) fijando la extensión `.php`.

### Comando de descubrimiento de archivos:

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ \
-u "http://SERVER_IP:PORT/blog/FUZZ.php"

```

## 4. Análisis de Respuestas

No basta con el código de estado; el tamaño de la respuesta (**Size**) es el indicador clave de contenido útil:

* **Size 0**: El archivo existe pero está vacío o no devuelve datos.
* **Size > 0**: Indica un archivo con lógica o contenido real (ej. 465 bytes), siendo este el objetivo prioritario para el análisis de vulnerabilidades.

> [!TIP]
> Si el servidor responde con 200 OK para archivos inexistentes (falsos positivos), utiliza el filtro `-fs [size]` para ignorar el tamaño de la página de error genérica.

```

---
