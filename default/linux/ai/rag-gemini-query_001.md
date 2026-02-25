---
chunk_id: technique::linux::ai::rag-gemini-query::001
domain: linux
chunk_type: technique
---

# Interfaz de consulta RAG: Gemini y Pinecone Vector Database

La herramienta `rag-gemini` permite realizar búsquedas semánticas sobre una base de datos de vectores en Pinecone, utilizando modelos de lenguaje de Gemini para contextualizar y responder consultas basadas en el contenido indexado.



## 1. Interfaz de Línea de Comandos (Comando Global)
El alias o binario `rag-gemini` proporciona la forma más rápida de interactuar con el índice sin necesidad de activar entornos manualmente.

- **Búsqueda estándar**: `rag-gemini "tu búsqueda"`
- **Ajuste de precisión (Top-K)**: `rag-gemini "LFI exploitation" --top-k 10`
- **Depuración (Modo Verbose)**: `rag-gemini "git commands" -v`
- **Gestión de Índices**: `rag-gemini --list-indexes`

## 2. Ejecución Técnica (Acceso al Script)
En caso de fallo del comando global o necesidad de modificar el comportamiento del script, se puede ejecutar directamente desde el entorno virtual.

### Procedimiento de ejecución manual:
```bash
# 1. Activar el entorno virtual de OpenSkills
source /root/.openskills/venv/bin/activate

# 2. Ejecutar el script principal indicando la ruta absoluta
python3 /home/kali/Desktop/RAG/src/query_gemini.py "query"

```

## 3. Parámetros de Configuración Críticos

* **--top-k**: Define cuántos fragmentos (chunks) similares recuperará de Pinecone antes de enviarlos a Gemini. Un valor más alto ofrece más contexto pero consume más tokens.
* **-v (Verbose)**: Útil para inspeccionar qué fragmentos específicos de la base de datos están siendo seleccionados por el algoritmo de similitud de coseno.

> [!NOTE]
> Asegúrate de que las variables de entorno `PINECONE_API_KEY` y `GEMINI_API_KEY` estén correctamente configuradas en tu `.bashrc` o `.zshrc` para que las consultas no fallen por falta de autenticación.

```

---
