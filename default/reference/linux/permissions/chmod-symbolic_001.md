---
chunk_id: reference::linux::permissions::chmod-symbolic::001
domain: reference
chunk_type: technique
---

### CHMOD Directorios 

En el modo simbólico, se utilizan letras para definir a quién se aplica el cambio y operadores para añadir o quitar permisos.

####  Lógica para Directorios
Para que una carpeta sea funcional, el permiso de **ejecución (x)** es indispensable para poder acceder a ella.

| Acción | Comando | Efecto |
| :--- | :--- | :--- |
| **Listar** | `chmod u+r dir` | Permite ver los nombres de archivos dentro. |
| **Entrar** | `chmod u+x dir` | Permite hacer `cd` al directorio. |
| **Modificar** | `chmod u+w dir` | Permite crear, borrar o renombrar archivos. |
| **Navegar** | `chmod u+rx dir` | Configuración mínima recomendada para lectura. |
| **Full** | `chmod u+rwx dir` | Control total sobre la carpeta. |



---

#### 🛠️ Modo Express (Simbólico)
Ideal para cambios rápidos sin calcular valores octales.

**Identificadores:**
- `u`: Dueño (User)
- `g`: Grupo (Group)
- `o`: Otros (Others)
- `a`: Todos (All)

**Operadores:**
- `+`: Añadir permiso.
- `-`: Quitar permiso.
- `=`: Asignar exactamente (pisando lo anterior).

 Ejemplos de uso rápido
 - **Dar lectura a todos:** `chmod a+r archivo`
 - **Dar lectura y ejecución a todos:** `chmod a+rx archivo`
 - **Quitar todo a todos:** `chmod a-rwx archivo`
 - **Hacer script ejecutable:** `chmod +x script.sh` (asume `a+x`)

---

#### 💡 Tip de Pentesting
Si durante una auditoría encuentras una carpeta con permisos de escritura para "otros" (`o+w`), es un vector potencial para subir scripts de enumeración como **LinPEAS** o realizar persistencia.
