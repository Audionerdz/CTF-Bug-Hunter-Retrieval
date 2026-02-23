---
chunk_id: cli::english::vectorization::single-file::001
domain: cli
chunk_type: technique
---

## Vectorize a Single File

```bash
# From repo root
cd /home/kali/Desktop/RAG

# Vectorize ONE file
vectorize /home/kali/Desktop/RAG/default/network/directory-fuzzing_001.md

# Or with full path
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py /home/kali/Desktop/RAG/default/network/directory-fuzzing_001.md

# Check result
echo "Vectorization complete!"
```
---

## Vectorize a Single File

```bash
# From repo root
cd /home/kali/Desktop/RAG

# Vectorize ONE file
python3 src/vectorize_canonical_openai.py ./docs/my-guide.md

# Check result
echo "Vectorization complete!"
```
