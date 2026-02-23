---
chunk_id: github::setup::working-directory::001
domain: github
chunk_type: technique
---

# ¿De Qué Carpeta Tengo que Estar Para Trabajar en Mi Repo?

## La Carpeta Correcta Es Esta:

```bash
/home/kali/Desktop/RAG
```

## Cómo Entrar a la Carpeta Correcta

```bash
# Desde cualquier lado, entra a tu repo
cd /home/kali/Desktop/RAG

# Verifica que estás en la carpeta correcta
pwd

# Deberías ver:
# /home/kali/Desktop/RAG
```

## Cómo Saber que Estás en la Carpeta Correcta

```bash
# Comando para ver dónde estás
pwd

# Resultado esperado:
# /home/kali/Desktop/RAG
```

## Una Vez Estés Adentro, TODOS Estos Comandos Funcionan

```bash
# Ver estado de tu repo
git status

# Ver cambios
git diff

# Preparar cambios
git add .

# Hacer commit
git commit -m "tu mensaje"

# Subir a GitHub
git push origin main

# Vectorizar contenido
python3 src/vectorize_canonical_openai.py ./docs/

# Buscar en tu base de conocimiento
python3 src/query_canonical_openai.py "tu pregunta"
```

## Resumen: TODO DESDE AQUÍ

```
/home/kali/Desktop/RAG  ← ESTARTE SIEMPRE AQUÍ
│
├── src/                ← Scripts Python (vectorizer, query)
├── docs/               ← Tus guías y documentación
├── default/            ← Chunks vectorizados
├── scripts/            ← Scripts Bash
├── config/             ← Configuración
├── CLI_CHEATSHEET.md   ← Guía CLI
└── .git/               ← Repositorio de Git
```
