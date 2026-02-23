---
chunk_id: technique::linux::shell::tty-upgrade::001
domain: linux
chunk_type: technique
---

### 🧰 Mejora de Shell con Pseudo TTY (Python)

```bash
# Paso 1: Spawn de la shell
python3 -c 'import pty; pty.spawn("/bin/bash")'

# Paso 2: Configuración de dimensiones (ajustar según tu terminal)
stty rows 50 cols 180

# Paso 3: Definir variable de entorno para colores y editores
export TERM=xterm
