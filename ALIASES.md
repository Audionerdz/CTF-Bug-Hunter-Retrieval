# Aliases para RAG System

Para facilitar el uso del sistema RAG, se han configurado dos aliases en `~/.bashrc` y `~/.zshrc`:

## Aliases disponibles

```bash
alias vectorize='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py'
alias query='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py'
```

## Uso

### Vectorizar un archivo individual
```bash
vectorize /home/kali/Desktop/RAG/default/network/file.md
```

### Vectorizar un directorio completo
```bash
vectorize /home/kali/Desktop/RAG/default/
```

### Hacer una consulta
```bash
query "tu pregunta aquí"
```

### Ejemplos
```bash
# Vectorizar
vectorize /home/kali/Desktop/RAG/default/network/directory-fuzzing_001.md

# Consultar
query "cómo vectorizar archivos"
query "ffuf directory fuzzing"
```

## Instalación

### Para Bash (~/.bashrc)
```bash
echo "alias vectorize='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py'" >> ~/.bashrc
echo "alias query='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py'" >> ~/.bashrc
source ~/.bashrc
```

### Para Zsh (~/.zshrc)
```bash
echo "alias vectorize='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py'" >> ~/.zshrc
echo "alias query='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py'" >> ~/.zshrc
source ~/.zshrc
```

## Verificar aliases

```bash
alias | grep -E 'vectorize|query'
```

Deberías ver:
```
alias query='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py'
alias vectorize='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py'
```

## Solución si los aliases no funcionan

1. Asegúrate de estar en zsh: `echo $SHELL` (debe mostrar `/bin/zsh`)
2. Abre una **nueva terminal** después de agregar los aliases
3. Verifica que estén en `~/.zshrc`: `grep -E "alias vectorize|alias query" ~/.zshrc`
