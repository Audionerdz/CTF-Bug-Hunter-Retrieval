---
chunk_id: reference::linux::permissions::sudo-privileges::001
domain: reference
chunk_type: technique
---

###  Sudo privileges 

```bash
sudo usermod -aG sudo tu_usuario
```

o en Kali (que usa grupo **sudo**):

```bash
sudo usermod -aG sudo ${USER}
```

Luego **cierra sesión y vuelve a entrar**.

---

### ✔ Si quieres darle permisos completos **solo a un folder**, sin sudo:

```bash
sudo chown -R kali:kali /ruta/del/folder
```

Eso te da control total sobre ese folder.

---
