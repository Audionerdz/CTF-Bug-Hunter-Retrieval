# 🚀 Quick Access - CLI Cheatsheet Guides

## Your CLI Guides Are Ready!

This document shows you how to use your new comprehensive CLI cheatsheet guides.

---

## 📖 Full Guides (Complete Reference)

### English Version
```bash
# Read the full English CLI cheatsheet
cat CLI_CHEATSHEET.md

# Or open in your editor
nano CLI_CHEATSHEET.md
code CLI_CHEATSHEET.md
vim CLI_CHEATSHEET.md
```

**Contents:**
- Absolute Beginner Setup
- Git Basics (Track Changes)
- Making Changes (Edit & Commit)
- Reverting & Fixing Mistakes
- Directory & File Operations
- Uploading to Remote (GitHub)
- Vectorization Workflow
- Script Reference Quick Fire

### Spanish Version
```bash
# Read the full Spanish CLI cheatsheet
cat GUIA_CLI_CHEATSHEET.md

# Or open in your editor
nano GUIA_CLI_CHEATSHEET.md
code GUIA_CLI_CHEATSHEET.md
vim GUIA_CLI_CHEATSHEET.md
```

**Contenidos:**
- Setup Absoluto para Principiantes
- Conceptos Básicos de Git
- Hacer Cambios (Editar y Confirmar)
- Revertir y Corregir Errores
- Operaciones con Directorios y Archivos
- Subir a GitHub
- Flujo de Vectorización
- Referencia Rápida de Scripts

---

## 🔍 Query Your Knowledge Base (RAG Search)

Your guides are **vectorized and searchable**!

### Search in English
```bash
# Example queries:
python3 src/query_canonical_openai.py "how to revert a commit"
python3 src/query_canonical_openai.py "how to vectorize files"
python3 src/query_canonical_openai.py "how to push to github"
python3 src/query_canonical_openai.py "directory operations"
python3 src/query_canonical_openai.py "git setup"
python3 src/query_canonical_openai.py "error recovery"
```

### Search in Spanish
```bash
# Example queries:
python3 src/query_canonical_openai.py "cómo revertir un commit"
python3 src/query_canonical_openai.py "cómo vectorizar archivos"
python3 src/query_canonical_openai.py "cómo subir a github"
python3 src/query_canonical_openai.py "operaciones de directorio"
python3 src/query_canonical_openai.py "setup de git"
python3 src/query_canonical_openai.py "recuperación de errores"
```

### Mixed Language Queries
```bash
python3 src/query_canonical_openai.py "git commit workflow"
python3 src/query_canonical_openai.py "staging files to repository"
python3 src/query_canonical_openai.py "vectorización y búsqueda"
```

---

## 📋 Common Queries & Usage

### Git Workflow Questions
```bash
python3 src/query_canonical_openai.py "git add staging commit push"
python3 src/query_canonical_openai.py "how to check git status"
python3 src/query_canonical_openai.py "revert changes before commit"
```

### File & Directory Operations
```bash
python3 src/query_canonical_openai.py "copy directory files"
python3 src/query_canonical_openai.py "upload files to repo"
python3 src/query_canonical_openai.py "directory structure"
```

### Vectorization Workflow
```bash
python3 src/query_canonical_openai.py "vectorize markdown"
python3 src/query_canonical_openai.py "pinecone storage"
python3 src/query_canonical_openai.py "semantic search"
```

### Troubleshooting
```bash
python3 src/query_canonical_openai.py "git cannot push"
python3 src/query_canonical_openai.py "python dependencies"
python3 src/query_canonical_openai.py "vectorization error"
```

---

## 🎯 Quick Command Reference

| Task | English Guide | Spanish Guide | Query Command |
|------|---------------|---------------|---------------|
| **Setup** | Sec 1 | Sec 1 | `query "git setup"` |
| **Git Status** | Sec 2 | Sec 2 | `query "git status"` |
| **Make Changes** | Sec 3 | Sec 3 | `query "edit commit"` |
| **Undo Mistakes** | Sec 4 | Sec 4 | `query "revert reset"` |
| **File Ops** | Sec 5 | Sec 5 | `query "copy move files"` |
| **Push/Pull** | Sec 6 | Sec 6 | `query "github push pull"` |
| **Vectorize** | Sec 7 | Sec 7 | `query "vectorize"` |
| **Quick Ref** | Sec 8 | Sec 8 | `query "commands reference"` |

---

## 🔬 Technical Details

### Vectorization Info
```bash
# View chunk registry (all vectorized chunks)
cat chunk_registry.json | python3 -m json.tool

# Check which chunks are available
cat chunk_registry.json | grep "cli::" | python3 -m json.tool
```

### Index Details
- **Index Name**: `rag-canonical-v1-emb3large`
- **Model**: OpenAI text-embedding-3-large (3072 dimensions)
- **Chunks**: 2 (1 English + 1 Spanish)
- **Vector Size**: 3072D
- **Status**: ✅ Active & Queryable

---

## 💡 Usage Tips

### Tip 1: Use Natural Language Queries
```bash
# Good - natural questions
python3 src/query_canonical_openai.py "I made a mistake, how do I undo it?"

# Also good - keywords
python3 src/query_canonical_openai.py "git reset soft hard"
```

### Tip 2: Query Multiple Times
Different phrasings return different results:
```bash
python3 src/query_canonical_openai.py "revert commit"
python3 src/query_canonical_openai.py "undo changes"
python3 src/query_canonical_openai.py "git restore"
```

### Tip 3: Combine with Grep for Offline Search
```bash
# Search locally without API call
grep -n "vectorize" CLI_CHEATSHEET.md
grep -n "vectorizar" GUIA_CLI_CHEATSHEET.md
```

### Tip 4: Create Custom Aliases (Optional)
```bash
# Add to ~/.bashrc or ~/.zshrc
alias cheatsheet-en='cat /home/kali/Desktop/RAG/CLI_CHEATSHEET.md'
alias cheatsheet-es='cat /home/kali/Desktop/RAG/GUIA_CLI_CHEATSHEET.md'
alias query-cli='python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py'

# Then use:
cheatsheet-en | less
query-cli "your question"
```

---

## 🗂️ File Locations

```
/home/kali/Desktop/RAG/
├── CLI_CHEATSHEET.md                    ← Full English guide
├── GUIA_CLI_CHEATSHEET.md               ← Full Spanish guide
├── CLI_GUIDES_QUICK_ACCESS.md           ← This file
└── default/
    ├── CLI_CHEATSHEET_ENGLISH.md        ← Vectorized English chunks
    └── CLI_CHEATSHEET_SPANISH.md        ← Vectorized Spanish chunks
```

---

## 🔄 Updating Your Guides

### To Add New Content
```bash
# 1. Edit the main guide
nano CLI_CHEATSHEET.md
# or
nano GUIA_CLI_CHEATSHEET.md

# 2. Update the chunked version
nano default/CLI_CHEATSHEET_ENGLISH.md
# or
nano default/CLI_CHEATSHEET_SPANISH.md

# 3. Re-vectorize
python3 src/vectorize_canonical_openai.py ./default/CLI_CHEATSHEET_ENGLISH.md
python3 src/vectorize_canonical_openai.py ./default/CLI_CHEATSHEET_SPANISH.md

# 4. Commit & Push
git add .
git commit -m "docs: Update CLI guides with new content"
git push origin main
```

---

## 📊 What's Inside

### Coverage Areas

**Git Operations** ✅
- Setup and configuration
- Checking status and changes
- Staging and committing
- Pushing and pulling
- Reverting and undoing

**File Management** ✅
- Directory operations
- File copying and moving
- Uploading to repository
- File deletion
- Directory structure

**Vectorization** ✅
- Single file vectorization
- Directory vectorization
- Batch operations
- Query workflow
- Troubleshooting

**Recovery** ✅
- Undo uncommitted changes
- Revert commits
- Merge conflict handling
- Error scenarios

**Reference** ✅
- Quick command table
- Common scenarios
- Pro tips
- Troubleshooting guide

---

## ✨ Features

✅ **Beginner-Friendly**: Start from zero knowledge  
✅ **Copy-Paste Ready**: Commands work immediately  
✅ **Bilingual**: English and Spanish  
✅ **Comprehensive**: 500+ lines each  
✅ **Searchable**: RAG-enabled semantic search  
✅ **Examples**: Real-world code examples  
✅ **Tables**: Quick reference cards  
✅ **Tips**: Pro tips and tricks  
✅ **Recovery**: Error handling guide  
✅ **GitHub Ready**: Push to repository  

---

## 🚀 Next Steps

1. **Read Your Guide**
   ```bash
   cat CLI_CHEATSHEET.md
   ```

2. **Try a Query**
   ```bash
   python3 src/query_canonical_openai.py "how to make a git commit"
   ```

3. **Use the Commands**
   Start using the commands from the guide!

4. **Share with Team**
   ```bash
   # Your guides are in GitHub
   https://github.com/Audionerdz/CTF-Bug-Hunter-Retrieval
   ```

---

## 📞 Questions?

All answers are in your vectorized knowledge base!

```bash
python3 src/query_canonical_openai.py "your question here"
```

---

**Created**: February 2026  
**Status**: ✅ Production Ready  
**Languages**: English + Spanish  
**Vectorization**: Complete  

