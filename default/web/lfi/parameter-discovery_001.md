---
chunk_id: technique::web::lfi::parameter-discovery::001
domain: web
chunk_type: technique
---

# Identificación de puntos de entrada para LFI

La inclusión de archivos locales (LFI) ocurre cuando una aplicación web permite a un usuario controlar el nombre o la ruta de un archivo que el servidor debe cargar. La fase crítica es la identificación de parámetros vulnerables, ya sean explícitos u ocultos.

## 1. Parámetros Críticos (Vectores Comunes)
Los parámetros que gestionan contenido dinámico o idiomas son los sospechosos primarios.

### A. Parámetros de Archivo y Navegación
* **Clásicos:** `file`, `page`, `path`, `include`, `inc`, `view`, `content`.
* **De Estructura:** `template`, `tpl`, `layout`, `theme`, `module`.
* **De Idioma:** `lang`, `language`, `locale`.

### B. Parámetros "Disfrazados" (Nomenclatura Funcional)
En aplicaciones modernas (MVC), el LFI puede esconderse en parámetros que cargan componentes:
* `controller`, `route`, `component`, `plugin`, `extension`, `engine`.

## 2. Descubrimiento de Parámetros Ocultos
Muchos vectores de LFI no están expuestos en formularios. Se deben auditar mediante fuzzing de parámetros (Parameter Fuzzing) buscando variables de desarrollo o depuración:
* **Variables de Entorno:** `debug`, `test`, `dev`, `config`, `cfg`.
* **Variables de Origen:** `source`, `src`, `backup`, `old`.

## 3. Funciones de Backend que Delatan LFI
Si se tiene acceso al código fuente o mensajes de error (Verbose Errors), las siguientes funciones indican una carga de archivos que podría ser vulnerable:

| Lenguaje | Funciones de Ejecución/Carga | Funciones de Solo Lectura |
| :--- | :--- | :--- |
| **PHP** | `include`, `require`, `include_once` | `file_get_contents`, `readfile`, `fopen` |
| **NodeJS** | `res.render`, `require` | `fs.readFile`, `fs.readFileSync` |
| **Java** | `import` | `FileInputStream`, `getResourceAsStream` |

## 4. Metodología de Confirmación Rápida
Para confirmar la vulnerabilidad antes de intentar un RCE:
1.  Identificar un parámetro que cargue contenido (Ej: `page=home`).
2.  Intentar romper la ruta lógica con `../`.
3.  Apuntar a un archivo estático conocido del sistema (Ej: `/etc/passwd` en Linux o `C:/windows/win.ini` en Windows).

> **WARNING:** En entornos de Bug Bounty, el éxito al leer `/etc/passwd` o un archivo `.env` ya representa un impacto crítico (Source Code Disclosure / Info Leak), incluso sin alcanzar ejecución de comandos (RCE).
