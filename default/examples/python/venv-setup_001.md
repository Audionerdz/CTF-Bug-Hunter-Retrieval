---
chunk_id: technique::python::env-config::venv-setup::001
domain: python
chunk_type: technique
---

###  Entornos Virtuales en Python (Venv)

Solución estándar para el error `externally-managed-environment` en sistemas modernos (Kali/Debian), permitiendo instalar dependencias de forma aislada sin comprometer el sistema global.

#### 🚀 Configuración del Entorno

```bash
# 1. Navegar al proyecto
cd ~/ruta/del/proyecto

# 2. Crear el entorno virtual (si falla: sudo apt install python3-venv)
python3 -m venv .venv
#.venv es el nombre de la carpeta que se creara 
# 3. Activar el entorno (Bash/Zsh)
source .venv/bin/activate

# 4. Actualizar pip e instalar requerimientos
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

|**Acción**|**Comando**|
|---|---|
|**Salir del entorno**|`deactivate`|
|**Borrar entorno**|`rm -rf .venv`|

```
