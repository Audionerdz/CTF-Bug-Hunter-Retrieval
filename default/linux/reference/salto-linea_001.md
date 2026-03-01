---
chunk_id: technique::linux::shell::salto-de-linea::line-continuation::001
domain: linux
chunk_type: technique
confidence: 5
reuse_level: 1
tags: [bash, shell-scripting, terminal-shortcuts, syntax, linux-basics]
---

# Uso de la barra invertida para la continuación de líneas en Linux

En la shell de Linux (Bash, Zsh, etc.), la barra invertida (`\`) se utiliza como un carácter de escape que, al colocarse al final de una línea, indica al intérprete que el comando continúa en la línea siguiente. Esto es fundamental para mantener la legibilidad de comandos extensos o scripts complejos.



## 1. Funcionamiento Técnico
Cuando el intérprete de comandos encuentra un `\` seguido inmediatamente por un salto de línea (tecla **Enter**), ignora ambos caracteres y trata la entrada de la línea siguiente como parte de la misma cadena de comandos.

### Regla de Oro:
No debe existir **ningún espacio ni carácter** después de la barra invertida. Si hay un espacio, la shell interpretará el `\` como un escape del espacio y ejecutará el comando prematuramente, resultando usualmente en un error de sintaxis.

## 2. Ejemplos Prácticos

### Comandos con múltiples parámetros
Ideal para herramientas de enumeración como `ffuf` o `nmap`:

```bash
ffuf -w wordlist.txt:FUZZ \
     -u [http://target.htb/FUZZ](http://target.htb/FUZZ) \
     -recursion \
     -v
