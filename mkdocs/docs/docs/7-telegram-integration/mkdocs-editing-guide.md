# MKDocs - Guía de Edición, Adición y Eliminación de Contenido

**Para modificar tu documentación HTML estática y regenerar PDF**

---

## 📁 Estructura de Archivos

```
mkdocs-unified-methodology/
├── docs/
│   ├── 1-intro/
│   ├── 2-chunking-methodology/
│   ├── 3-pinecone-guide/
│   ├── 4-rag-architecture/
│   ├── 5-advanced-topics/
│   ├── 6-manual-pinecone-operations/
│   ├── 7-telegram-integration/        ← AQUÍ ESTÁN TUS ARCHIVOS
│   │   ├── index.md
│   │   ├── vectorizer-complete-guide.md
│   │   ├── vectorization-usage-guide.md
│   │   ├── vectorizer-modular.md      ← NUEVO
│   │   ├── telegram_bot_daemon.md
│   │   ├── query-agent-integration.md
│   │   └── ... (otros archivos)
│   └── index.md
├── mkdocs.yml                         ← CONFIGURACIÓN
├── venv/                              ← Python environment
└── site/                              ← GENERADO (no editar)
```

---

## 🎯 Editar Contenido Existente

### Paso 1: Abre el archivo

```bash
cd /root/mkdocs-unified-methodology/
nano docs/7-telegram-integration/vectorizer-complete-guide.md
```

### Paso 2: Realiza cambios

- Edita markdown normalmente
- Guarda (Ctrl+X, Y, Enter en nano)

### Paso 3: Rebuild y sirve

```bash
mkdocs build --clean
mkdocs build
mkdocs serve
```

### Paso 4: Verifica en navegador

```
http://localhost:8000/7-telegram-integration/vectorizer-complete-guide/
```

Los cambios se ven **inmediatamente**.

---

## ➕ Agregar Contenido Nuevo

### Paso 1: Crea el archivo

```bash
cat > docs/7-telegram-integration/mi-nueva-pagina.md << 'EOF'
# Titulo de Mi Nueva Página

Contenido aquí...
EOF
```

### Paso 2: Edita mkdocs.yml

Agrega la entrada en la sección correspondiente:

```yaml
   - Part 7 - Telegram Integration & Scripts:
       - Introduction: 7-telegram-integration/index.md
       - Vectorizer Modular: 7-telegram-integration/vectorizer-modular.md
       - Mi Nueva Página: 7-telegram-integration/mi-nueva-pagina.md
```

**Importante**: Indentación con spaces (no tabs).

### Paso 3: Rebuild

```bash
mkdocs build
mkdocs serve
```

Tu nueva página aparecerá en la navegación.

---

## ❌ Eliminar Contenido

### Paso 1: Elimina el archivo

```bash
rm docs/7-telegram-integration/pagina-vieja.md
```

### Paso 2: Edita mkdocs.yml

Busca y elimina la entrada:

```yaml
       - Pagina Vieja: 7-telegram-integration/pagina-vieja.md    ← QUITA ESTA LÍNEA
```

### Paso 3: Rebuild

```bash
mkdocs build --clean
mkdocs serve
```

---

## 📄 Crear PDF Actualizado

### Opción A: PDF durante build

```bash
mkdocs build --with-pdf
```

El PDF está en: `site/unified-rag-methodology.pdf`

### Opción B: Limpiar y regenerar TODO

```bash
mkdocs build --clean --with-pdf
```

Esto:
1. Elimina la carpeta `site/` anterior
2. Reconstruye TODO el HTML
3. Genera PDF nuevo

---

## 🔄 Workflow Completo

### Editar 1 página

```bash
nano docs/7-telegram-integration/archivo.md
mkdocs build
mkdocs serve
```

### Agregar 3 páginas nuevas

```bash
# 1. Crea los 3 archivos
cat > docs/7-telegram-integration/page1.md << 'EOF'
# Page 1
Content...
EOF

# 2. Edita mkdocs.yml (agrega 3 entradas)
nano mkdocs.yml

# 3. Rebuild con PDF
mkdocs build --clean --with-pdf

# 4. Sirve
mkdocs serve
```

### Publicar cambios

```bash
# 1. Build final
mkdocs build --clean --with-pdf

# 2. Copia site/ a servidor
cp -r site/* /var/www/html/docs/

# 3. ¡Listo!
```

---

## 📝 Sintaxis Markdown

```markdown
# Título 1
## Título 2
### Título 3

**Bold**
*Italic*
`código`

```python
bloque de código
```

- Lista
- Items

| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |

[Enlace](url)
![Imagen](url)
```

---

## ⚙️ Configuración (mkdocs.yml)

### Cambiar tema

```yaml
theme:
  name: material
```

### Cambiar colores

```yaml
theme:
  palette:
    scheme: slate
    primary: blue
    accent: cyan
```

### Cambiar título

```yaml
site_name: Mi Nuevo Título
site_description: Mi descripción
```

---

## 🚀 Deploy a Producción

### GitHub Pages

```bash
pip install ghp-import
mkdocs build
ghp-import -p site
```

### Netlify

Arrastra carpeta `site/` a netlify.com

### Servidor propio

```bash
scp -r site/* usuario@servidor:/var/www/html/docs/
```

---

## 🔍 Verificación Antes de Publicar

```bash
# 1. Build (revela errores)
mkdocs build

# 2. Sirve localmente
mkdocs serve

# 3. Abre http://localhost:8000
# - Navega todas las páginas
# - Verifica enlaces
# - Comprueba formato

# 4. Genera PDF
mkdocs build --clean --with-pdf

# 5. Abre PDF y verifica
```

---

## ❌ Errores Comunes

| Error | Solución |
|-------|----------|
| Directory not found | Navega a `mkdocs-unified-methodology/` |
| Failed to build | Revisa indentación en mkdocs.yml (spaces) |
| Page not found | Crea archivo o quita entrada de nav |
| mkdocs not found | `pip install mkdocs mkdocs-material` |

---

## 💾 Control de Versiones

```bash
git init
git add .
git commit -m "Update documentation"
git push origin main
```

---

## 🎯 Resumen Rápido

| Acción | Comando |
|--------|---------|
| Editar página | `nano docs/archivo.md` |
| Agregar página | Crea archivo + edita mkdocs.yml |
| Eliminar página | `rm docs/archivo.md` + edita mkdocs.yml |
| Build | `mkdocs build` |
| Servir | `mkdocs serve` |
| PDF | `mkdocs build --with-pdf` |

---

**MKDocs lo hace automático. Solo edita markdown y HTML se genera solo!** 🚀
