---
chunk_id: reference::linux::permissions::chmod-numeric::001
domain: reference
chunk_type: technique
---

##  Permisos Numéricos (Modo Octal)

La representación numérica se basa en la suma de valores para cada nivel (Dueño, Grupo, Otros).

| Valor | Permiso | Acción |
| :--- | :--- | :--- |
| **4** | `r` | Lectura (Read) |
| **2** | `w` | Escritura (Write) |
| **1** | `x` | Ejecución (Execute) |



###  Ejemplos Comunes

| Comando | Representación Simbólica | Uso Típico |
| :--- | :--- | :--- |
| `chmod 700` | `rwx------` | Privacidad total (Solo el dueño accede). |
| `chmod 755` | `rwxr-xr-x` | Scripts o binarios públicos (Todos leen/ejecutan). |
| `chmod 644` | `rw-r--r--` | Archivos de texto o configs (Todos leen). |
| `chmod 600` | `rw-------` | Llaves SSH o archivos sensibles. |
| `chmod 777` | `rwxrwxrwx` | **Peligro:** Acceso total para todos. |
