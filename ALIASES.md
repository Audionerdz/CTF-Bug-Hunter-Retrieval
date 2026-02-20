# Bash Aliases para RAG System

Para facilitar el uso del sistema RAG, se han configurado dos aliases en `~/.bashrc`:

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

## Instalación manual

Si los aliases no aparecen después de abrir una nueva terminal, añade manualmente a `~/.bashrc`:

```bash
echo "alias vectorize='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py'" >> ~/.bashrc
echo "alias query='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py'" >> ~/.bashrc
source ~/.bashrc
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
