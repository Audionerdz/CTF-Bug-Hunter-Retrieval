---
chunk_id: cli::spanish::vectorization::directory::001
domain: cli
chunk_type: guide
category: vectorization
confidence: high
reuse_level: universal
tags: [vectorization, directorio, batch, spanish]
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
