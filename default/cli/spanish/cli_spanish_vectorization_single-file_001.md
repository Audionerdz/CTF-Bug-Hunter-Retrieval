---
chunk_id: cli::spanish::vectorization::single-file::001
domain: cli
chunk_type: guide
category: vectorization
confidence: high
reuse_level: universal
tags: [vectorization, archivo, individual, spanish]
---

## Vectorizar un Archivo Individual

```bash
# Desde la raíz del repo
cd /home/kali/Desktop/RAG

# Vectorizar UN archivo
vectorize /home/kali/Desktop/RAG/default/network/directory-fuzzing_001.md

# O con ruta completa
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py /home/kali/Desktop/RAG/default/network/directory-fuzzing_001.md

# Verificar resultado
echo "¡Vectorización completa!"
```
---

## Vectorizar un Archivo Individual

```bash
# Desde la raíz del repositorio
cd /home/kali/Desktop/RAG

# Vectoriza UN archivo
python3 src/vectorize_canonical_openai.py ./docs/mi-guia.md

# Ver resultado
echo "Vectorización completa!"
```
