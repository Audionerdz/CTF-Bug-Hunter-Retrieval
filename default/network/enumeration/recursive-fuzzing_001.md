---
chunk_id: technique::network::enumeration::recursive-fuzzing::001
domain: network
chunk_type: technique
---

# Enumeración web avanzada mediante Fuzzing Recursivo con ffuf

El fuzzing recursivo es una técnica que automatiza el descubrimiento de contenido en profundidad. Cuando `ffuf` identifica un directorio válido, inicia automáticamente un nuevo escaneo dentro de esa ruta, permitiendo descubrir estructuras de carpetas anidadas sin intervención manual.



## 1. Flags Críticos de Recursión
Para activar y controlar el comportamiento recursivo, se utilizan modificadores específicos que limitan el alcance y definen los objetivos.

- **-recursion**: Activa la capacidad de iniciar nuevos escaneos sobre los directorios encontrados.
- **-recursion-depth [n]**: Define el nivel máximo de anidación. Un valor de `1` fuzzea el directorio principal y los subdirectorios encontrados inmediatamente después.
- **-e [extensiones]**: Especifica las extensiones de archivo a buscar (Ej: `.php`, `.html`). Es vital para lenguajes específicos.
- **-v (Verbose)**: Muestra la URL completa en los resultados. Es indispensable en escaneos recursivos para saber exactamente en qué subcarpeta reside cada hallazgo.

## 2. Ejemplos de Implementación

### Escaneo de profundidad controlada
Este comando busca archivos PHP hasta un segundo nivel de profundidad:

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ \
-u [http://archive.academy.htb](http://archive.academy.htb):PORT/FUZZ \
-recursion -recursion-depth 2 -e .php -v

```

### Escaneo Multi-extensión con Salida de Datos

Para guardar los resultados en un formato procesable (JSON) y buscar múltiples tipos de archivos:

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/raft-small-directories.txt:FUZZ \
-u "http://SERVER_IP:PORT/FUZZ" \
-recursion -recursion-depth 2 \
-e .php,.html \
-o resultados_recursivos.json

```

## 3. Mejores Prácticas

* **Control de Carga**: La recursión aumenta exponencialmente el número de peticiones. Use `-recursion-depth` con precaución para evitar escaneos infinitos o denegaciones de servicio accidentales.
* **Diccionarios**: Para recursión, se recomiendan wordlists de tamaño pequeño o medio (como `raft-small-directories.txt`) para mantener un tiempo de ejecución razonable.
* **Output**: El uso de `-o` es altamente recomendado en este modo, ya que la cantidad de datos generada puede ser difícil de gestionar visualmente en la terminal.

> [!NOTE]
> La recursión solo ocurre sobre hallazgos que el servidor identifica como directorios (usualmente códigos 301 o 200 con contenido tipo directorio).

```

---
