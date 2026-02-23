# Aliases para RAG System

Para facilitar el uso del sistema RAG, se han configurado aliases en `~/.bashrc` y `~/.zshrc`:

## Aliases disponibles

```bash
alias vectorize='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py'
alias query='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_fast.py'
alias rag-chat='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/rag_terminal.py'
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

### Chat interactivo con RAG (LangChain + Gemini)
```bash
rag-chat
```

### Ejemplos
```bash
# Vectorizar
vectorize /home/kali/Desktop/RAG/default/network/directory-fuzzing_001.md

# Consultar
query "cómo vectorizar archivos"
query "ffuf directory fuzzing"

# Chat interactivo (LangChain + Pinecone + Gemini)
rag-chat
# > qué es LFI y cómo explotarlo
# > técnicas de SQL injection
# > exit
```

## Instalación

### Para Zsh (~/.zshrc)
```bash
echo "alias vectorize='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py'" >> ~/.zshrc
echo "alias query='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_fast.py'" >> ~/.zshrc
echo "alias rag-chat='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/rag_terminal.py'" >> ~/.zshrc
source ~/.zshrc
```

## Verificar aliases

```bash
alias | grep -E 'vectorize|query|rag-chat'
```

Deberías ver:
```
alias query='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py'
alias vectorize='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py'
alias rag-chat='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/rag_terminal.py'
```

## Solución si los aliases no funcionan

1. Asegúrate de estar en zsh: `echo $SHELL` (debe mostrar `/bin/zsh`)
2. Abre una **nueva terminal** después de agregar los aliases
3. Verifica que estén en `~/.zshrc`: `grep -E "alias vectorize|alias query" ~/.zshrc`
