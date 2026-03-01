---
chunk_id: technique::linux::admin::env-config::001
domain: linux
chunk_type: technique
---

### Anadir bin y scripts  al Path 

Para anadir un plugin a una variable conseguimos en que carpeta esta el plugin primero y luego hacemos:

```bash
echo 'export PATH=$PATH:~/go/bin' >> ~/.zshrc
source ~/.zshrc

```



Si escribes directamente:

```bash
export PATH="$PATH:/opt/miplugin/bin"
```

✅ **Sí lo añades al PATH**
❗ **Pero solo para esa sesión actual de la terminal**



Si quieres que sea permanente, entonces debes guardarlo en tu archivo de configuración:

Para zsh:

```bash
echo 'export PATH="$PATH:/opt/miplugin/bin"' >> ~/.zshrc
source ~/.zshrc
```

Para bash:

```bash
echo 'export PATH="$PATH:/opt/miplugin/bin"' >> ~/.bashrc
source ~/.bashrc
```
