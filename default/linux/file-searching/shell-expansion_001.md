---
chunk_id: technique::linux::file-searching::shell-expansion::001
domain: linux
chunk_type: technique
---

### 3. El truco del Shell (Expansion de comodines)

No solo sirven para `find`. Puedes usarlos directamente con comandos como `ls`, `cat` o `rm`:

- **Leer todos los archivos de una carpeta de una vez:**
    
    ```bash
    cat /opt/wftpserver/Data/Sessions/*.session
    ```
    
    Esto le dira a la terminal: "concatena todos los archivos que terminen en .session en esta ruta".
