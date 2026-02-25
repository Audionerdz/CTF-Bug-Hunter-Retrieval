---
chunk_id: technique::web::fuzzing::value-discovery::001
domain: web
chunk_type: technique
---

# Identificación de valores válidos mediante Fuzzing con ffuf

El Value Fuzzing es la técnica empleada una vez que se ha descubierto un parámetro válido (vía GET o POST). Consiste en probar sistemáticamente diferentes datos como IDs, nombres de usuario o tokens para observar cambios en la respuesta del servidor que indiquen una ejecución exitosa.



## 1. Preparación de Diccionarios (Wordlists)
Dependiendo del tipo de parámetro encontrado, se pueden utilizar listas pre-existentes o generar secuencias personalizadas.

### Generación de secuencias numéricas en Bash
Para parámetros de tipo ID secuencial, se puede crear una lista rápidamente desde la terminal:
- **Comando**: `for i in $(seq 1 1000); do echo $i >> ids.txt; done`
- **Resultado**: Crea el archivo `ids.txt` con valores del 1 al 1000.

### Diccionarios de Identidad (SecLists)
Para parámetros relacionados con usuarios o nombres, se recomiendan estas rutas:
- `/usr/share/seclists/Usernames/xato-net-10-million-usernames.txt`
- `/usr/share/seclists/Usernames/Names/names.txt`

## 2. Ejecución de Fuzzing de Valores
A diferencia del descubrimiento de parámetros, aquí el marcador `FUZZ` se coloca específicamente en la posición del **valor**, manteniendo el nombre del parámetro fijo.

### Ejemplo de comando POST para Usernames:
```bash
ffuf -w /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt:FUZZ \
-u [http://faculty.academy.htb](http://faculty.academy.htb):PORT/script.php \
-X POST -d 'username=FUZZ' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-fs [tamaño_a_filtrar]

```

> [!WARNING]
> Es vital que el nombre del parámetro (ej: `username` o `id`) sea el hallazgo confirmado en la fase previa de Parameter Fuzzing.

## 3. Validación de Resultados con curl

Tras obtener un "hit" (una respuesta con tamaño o código de estado distinto), se debe validar manualmente para observar el contenido de la respuesta.

### Ejemplo de validación manual:

```bash
curl [http://admin.academy.htb](http://admin.academy.htb):PORT/admin/admin.php \
-X POST -d 'id=73' \
-H 'Content-Type: application/x-www-form-urlencoded'

```

## 4. Diferenciación Crítica de Conceptos

* **Parameter Fuzzing**: Busca el nombre de la variable o "llave" (Ej: `?FUZZ=valor`).
* **Value Fuzzing**: Busca el dato o "contenido" (Ej: `?id=FUZZ`).

El éxito en esta fase depende de usar el filtro `-fs` adecuadamente para ignorar el "ruido" de las respuestas negativas constantes.

```

---
