---
chunk_id: technique::web::git-leak::source-analysis::001
domain: web
chunk_type: technique
---

### Exfiltración y Análisis de Repositorios .Git Expuestos


Técnica utilizada cuando un servidor web permite el acceso al directorio `.git`, lo que permite reconstruir el código fuente de la aplicación para buscar vulnerabilidades lógicas.

#### Fase 1: Descarga del Repositorio
Existen múltiples métodos según las restricciones del servidor.

```bash
# Opción A: Clonado directo (si el servidor lo permite)
git clone http://target.htb/.git target_leak

# Opción B: GitDumper (Recomendado para CTF)
# Requiere: pip install git-dumper
git-dumper http://target.htb/.git/ target_leak

# Opción C: Wget (Si falla el protocolo git)
wget -r --no-parent http://target.htb/.git/
````

#### Fase 2: Búsqueda Proactiva de Vulnerabilidades (Grep)

Una vez reconstruido el código, busca patrones que indiquen debilidades en la lógica o credenciales hardcodeadas.

```bash
# Credenciales y sesiones
grep -RiE "password|admin|user|role|session" -n .

# Funciones peligrosas (RCE/LFI)
grep -RiE "eval|include|require|system|exec" -n .

# Puntos de entrada de datos
grep -RiE "POST|GET|REQUEST" -n .
```

#### Fase 3: Identificación de Archivos Críticos

Archivos que suelen contener la lógica de negocio o la conexión a la base de datos:

| Archivo              | Objetivo del Análisis                                             |
| -------------------- | ----------------------------------------------------------------- |
| config.php / db.php  | Credenciales de DB y API keys.                                    |
| auth.php / login.php | Bypass de autenticación y manejo de sesiones.                     |
| rules_engine.php     | Análisis de lógica de negocio (frecuente en máquinas tipo Gavel). |
| *.php en /engine/    | Backend core donde suelen residir los fallos de procesamiento.    |

#### Post-Análisis

Si el repo está incompleto, usa:

```bash
git checkout -- .
```

dentro de la carpeta descargada para intentar restaurar los archivos que faltan en el working directory.
