---
chunk_id: technique::web::lua-rce::sandbox-escape::001
domain: web
chunk_type: technique
---

### RCE 

### Lua Sandbox Escape 

- **`anonymous\0]]`**: Esta es la parte de "escape". El atacante asume que el servidor ya tiene un código Lua ejecutándose (probablemente dentro de una cadena de texto). El `\0` (byte nulo) y los corchetes `]]` se usan para "romper" la lógica original del programa y forzar al servidor a leer lo que viene a continuación como un comando nuevo.
    
- **`local h = io.popen("id")`**: Aquí empieza la acción real. `io.popen` es una función de Lua que abre un canal con el sistema operativo. En este caso, ejecuta el comando **`id`**, que en sistemas Linux/Unix devuelve el nombre de usuario y los privilegios actuales (uid, gid).
    
- **`local r = h:read("*a")`**: Esta línea lee toda la salida generada por el comando `id` y la guarda en la variable `r`.
    
- **`h:close()`**: Cierra el proceso que se abrió para ejecutar el comando (buena práctica de programación, incluso en exploits).
    
- **`print(r)`**: Intenta imprimir la respuesta del comando. Si el servidor es vulnerable y devuelve errores o salidas al usuario, el atacante verá algo como `uid=33(www-data) gid=33(www-data)`.
    
- **`--`**: Estos son guiones de comentario en Lua. Se ponen al final para "anular" cualquier código que viniera después en el script original del servidor, evitando que el programa falle y permitiendo que la inyección pase desapercibida.
