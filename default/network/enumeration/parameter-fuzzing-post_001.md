---
chunk_id: technique::network::enumeration::parameter-fuzzing-post::001
domain: network
chunk_type: technique
---

# Enumeración de parámetros POST mediante Fuzzing con ffuf

El fuzzing de parámetros POST se utiliza para descubrir variables ocultas que se envían en el cuerpo (body) de una petición HTTP en lugar de la URL. Esta técnica es crítica para interactuar con formularios, APIs o scripts que no aceptan datos vía GET.

## 1. Diferencias Técnicas (GET vs POST)
A diferencia de GET, las peticiones POST requieren la especificación explícita del método y, frecuentemente, del tipo de contenido (Content-Type) para que el servidor procese los datos correctamente.

## 2. Configuración de ffuf para POST
Para realizar el descubrimiento, se utiliza el parámetro `-d` para definir el cuerpo de la data y el marcador `FUZZ` para el nombre del parámetro.

### Comando de Ejecución
```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ \
-u http://faculty.academy.htb:PORT/script.php \
-X POST \
-d 'FUZZ=key' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-fs [size]
```

**Parámetros específicos:**
* `-X POST`: Define el método de envío.
* `-d 'FUZZ=key'`: Indica los datos del cuerpo. El valor `key` es un marcador de posición (dummy value).
* `-H 'Content-Type: ...'`: Cabecera obligatoria en PHP para que el servidor reconozca los datos del formulario.

## 3. Verificación con curl
Una vez que `ffuf` identifica un parámetro válido (por ejemplo: `id`), se debe verificar manualmente enviando una petición POST estructurada.

```bash
# Verificación manual del parámetro encontrado
curl http://admin.academy.htb:PORT/admin/admin.php \
-X POST \
-d 'id=key' \
-H 'Content-Type: application/x-www-form-urlencoded'
```

## 4. Análisis de Resultados
Un parámetro es considerado "válido" si la respuesta del servidor cambia respecto a la respuesta base (por ejemplo, si deja de dar un error genérico y devuelve un mensaje como `Invalid id!`).

> **IMPORTANT:** El éxito del fuzzing POST depende totalmente de incluir el header `Content-Type`. Sin este, muchos backends ignorarán el contenido enviado en `-d`.
