---
chunk_id: technique::linux::shell::repair-zsh-history::001
domain: linux
chunk_type: technique
confidence: 5
reuse_level: 1
tags: [zsh, reparar, repair, fix, terminal, troubleshooting, history, kali-linux]
---

# Reparación de historial corrupto en ZSH

Es común que, tras un apagado inesperado o un fallo de memoria, el archivo `.zsh_history` se corrompa, mostrando errores al intentar usar flecha arriba o buscar comandos anteriores. Este procedimiento extrae los datos legibles y reconstruye el archivo.



## 1. Comando de Recuperación (One-liner)
Ejecuta esta secuencia para renombrar, limpiar, recargar y eliminar el rastro del archivo dañado:

```bash
mv ~/.zsh_history ~/.zsh_history_bad && strings ~/.zsh_history_bad > ~/.zsh_history && fc -R ~/.zsh_history && rm ~/.zsh_history_bad

```

## 2. Desglose de Operaciones

Para entender qué está ocurriendo bajo el capó:

* **`mv ~/.zsh_history ~/.zsh_history_bad`**: Mueve el archivo dañado a una ubicación temporal para que no estorbe.
* **`strings ~/.zsh_history_bad > ~/.zsh_history`**: La utilidad `strings` filtra el archivo binario dañado y solo extrae las secuencias de texto legibles, guardándolas en un archivo nuevo y limpio.
* **`fc -R ~/.zsh_history`**: Fuerza a la sesión actual de ZSH a leer de nuevo el archivo del historial (Recargar).
* **`rm ~/.zsh_history_bad`**: Limpieza final eliminando el archivo corrupto original.

## 3. Solución Radical (Empezar de Cero)

Si el daño es estructural y el comando anterior no resuelve el error, la única opción es purgar el historial completamente. **Nota: Esto borrará todos los comandos guardados.**

```bash
rm ~/.zsh_history && logout

```

Al volver a iniciar sesión, ZSH creará automáticamente un archivo de historial nuevo y vacío, eliminando cualquier mensaje de error.

> [!TIP]
> Para evitar futuras corrupciones, asegúrate de cerrar tus sesiones de terminal con `exit` o `logout` antes de apagar tu máquina virtual o equipo físico.

```

---

