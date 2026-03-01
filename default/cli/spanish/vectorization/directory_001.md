---
chunk_id: cli::spanish::vectorization::directory::001
domain: cli
chunk_type: technique
---

## Vectorizar un Directorio Completo

```bash
# Vectorizar todos los archivos en default/
vectorize /home/kali/Desktop/RAG/default/

# O con ruta completa
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py /home/kali/Desktop/RAG/default/

# Vectorizar subdirectorio específico
vectorize /home/kali/Desktop/RAG/default/network/

# Vectorizar repositorio completo
vectorize /home/kali/Desktop/RAG/

# El output mostrará los chunks creados
```
---

## Vectorizar un Directorio Completo

```bash
# Vectoriza todos los archivos en docs/
python3 src/vectorize_canonical_openai.py ./docs/

# Vectoriza el repositorio completo
python3 src/vectorize_canonical_openai.py .

# Resultado mostrará chunks creados
```
