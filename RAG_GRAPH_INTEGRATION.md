# RAG-Graph Integration Guide

## Overview

RAG-Graph es un módulo de visualización de conocimiento que se integra al repositorio RAG existente sin afectar funcionalidades actuales. Está completamente aislado pero permite visualizar las conexiones entre chunks como un grafo relacional similar a txtai.

## Arquitectura de Integración

### Aislamiento (No-Breaking Changes)

```
RAG Repository
├── atlas_engine/       [Existing] ✓ Unchanged
├── src/                [Existing] ✓ Unchanged
├── default/            [Shared]   ✓ Read-only access for RAG-Graph
├── config.py           [Existing] ✓ Unchanged
├── requirements.txt    [Existing] ✓ Unchanged
├── Dockerfile          [Existing] ✓ Unchanged
├── docker-compose.yml  [Modified] + Added rag-graph service
│
└── rag_graph/          [NEW]      ✓ Completely isolated module
    ├── models/         Data structures
    ├── builders/       Graph construction
    ├── api/            REST API server
    ├── visualization/  Frontend components (Phase 2)
    ├── storage/        Persistence layer
    ├── tests/          Comprehensive test suite
    └── examples/       Usage examples
```

### Integración Docker

```yaml
docker-compose.yml
├── atlas (existing)
│   ├── Builds from: Dockerfile
│   ├── Image: atlas-engine:local
│   └── Network: rag-network
│
└── rag-graph (new)
    ├── Builds from: rag_graph/Dockerfile.rag-graph
    ├── Image: rag-graph:local
    ├── Port: 8001 (REST API)
    ├── Network: rag-network (shared)
    ├── Depends on: atlas (service_started)
    └── Read-only access to: ./default
```

## Rama de Desarrollo

```
main (stable)
└── rag-graph (active development)
    ├── Phase 1: Core (completed)
    │   ✓ Data models
    │   ✓ GraphBuilder
    │   ✓ JSON/GraphML export
    │   ✓ Basic REST API
    │   ✓ Smoke tests
    │
    ├── Phase 2: Visualization (next)
    │   ○ D3.js/Cytoscape rendering
    │   ○ Interactive HTML frontend
    │   ○ Graph filtering and search
    │
    └── Phase 3: Advanced (future)
        ○ Neo4j integration
        ○ Pattern matching
        ○ Graph analytics
```

## Flujo de Desarrollo

### Cambios Locales

```bash
# 1. Trabajar en rama rag-graph
git checkout rag-graph

# 2. Hacer cambios al módulo rag_graph/
vim rag_graph/builders/graph_builder.py

# 3. Ejecutar tests
pytest rag_graph/tests/ -v

# 4. Ejecutar smoke tests
python rag_graph/tests/smoke_tests.py

# 5. Comitear cambios
git add rag_graph/
git commit -m "feat: descripción del cambio"
```

### Pruebas con Docker Compose

```bash
# Build images
docker-compose build

# Run entire stack with RAG-Graph
docker-compose up

# Access RAG-Graph API
curl http://localhost:8001/health
curl http://localhost:8001/api/graph/stats

# Run smoke tests in container
docker-compose run --rm rag-graph python rag_graph/tests/smoke_tests.py

# View logs
docker-compose logs -f rag-graph
```

### Pull Requests y Merges

```bash
# Cuando Phase 1 está completo:
git checkout main
git pull origin main
git merge rag-graph
git push origin main

# O mantener rama activa para desarrollo continuo
# y hacer cherry-picks de cambios estables
```

## Componentes Principales

### 1. Modelos de Datos (`rag_graph/models/`)

**Node.py**
- `NodeType`: Enumeration de 15 tipos de nodos
- `Node`: Clase de datos para nodos del grafo
- `NodeCollection`: Contenedor para gestionar nodos

**Edge.py**
- `EdgeType`: Enumeration de 12 tipos de relaciones
- `Edge`: Clase de datos para aristas
- `EdgeCollection`: Contenedor para gestionar aristas

**Metadata.py**
- `ChunkMetadata`: Extrae metadata de YAML frontmatter
- `GraphMetadataExtension`: Metadata opcional para HTB/CTF
- `ChunkParser`: Utilidad para parsear archivos markdown

### 2. Constructor de Grafo (`rag_graph/builders/`)

**GraphBuilder.py**
```python
builder = GraphBuilder(chunks_dir=Path("./default"))
builder.build_graph(include_core_topics=True)
builder.save_to_json(Path("graph.json"))
builder.save_to_graphml(Path("graph.graphml"))
stats = builder.get_stats()
```

Funcionalidad:
- Crea 4 nodos de fases de ataque
- Crea 8 nodos de dominios de conocimiento
- Procesa chunks de `default/`
- Crea aristas entre chunks y dominios
- Exporta a JSON y GraphML

### 3. API REST (`rag_graph/api/`)

**Server.py** (FastAPI)

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/graph` | GET | Grafo completo |
| `/api/graph/stats` | GET | Estadísticas |
| `/api/graph/nodes` | GET | Lista de nodos |
| `/api/graph/edges` | GET | Lista de aristas |
| `/api/node/{id}` | GET | Nodo específico |
| `/api/node/{id}/neighbors` | GET | Vecinos del nodo |
| `/api/graph/rebuild` | POST | Reconstruir grafo |

### 4. Tests (`rag_graph/tests/`)

**test_models.py**
- Tests de Node, Edge y Collections
- Serialización/deserialización
- Validaciones

**test_graph_builder.py**
- Tests de construcción de grafo
- Procesamiento de chunks
- Exportación a formatos
- Tests con chunks reales

**smoke_tests.py**
- Tests rápidos para CI/CD
- Validación de imports
- Construcción básica de grafo
- Exportación JSON

Ejecutar:
```bash
pytest rag_graph/tests/ -v              # Todos los tests
pytest rag_graph/tests/ --cov=rag_graph # Con coverage
python rag_graph/tests/smoke_tests.py   # Smoke tests
```

## Tipos de Nodos

### Fases de Ataque (Attack Phases)

| Node ID | Label | Color | Severidad |
|---------|-------|-------|-----------|
| `enumeration` | Enumeration | #FF6B6B | CRITICAL |
| `foothold` | Foothold | #FF6B6B | CRITICAL |
| `post_exploitation` | Post Exploitation | #FF6B6B | CRITICAL |
| `privilege_escalation` | Privilege Escalation | #FF6B6B | CRITICAL |

### Dominios de Conocimiento (Knowledge Domains)

| Node ID | Label | Color | Severidad |
|---------|-------|-------|-----------|
| `rag` | RAG & NLP | #4ECDC4 | HIGH |
| `python` | Python Programming | #4ECDC4 | HIGH |
| `web_security` | Web Security | #4ECDC4 | HIGH |
| `linux_security` | Linux Security | #4ECDC4 | HIGH |
| `windows_security` | Windows Security | #4ECDC4 | HIGH |
| `networking` | Networking | #4ECDC4 | HIGH |
| `cryptography` | Cryptography | #4ECDC4 | HIGH |
| `reverse_engineering` | Reverse Engineering | #4ECDC4 | HIGH |

### Nodos de Contenido (Content Nodes)

Creados automáticamente desde chunks:
- `chunk` - Chunk individual
- `technique` - Técnica de seguridad
- `exploit` - Código de explotación
- `procedure` - Procedimiento paso a paso
- `guideline` - Mejores prácticas
- `reference` - Referencia rápida
- `concept` - Concepto

## Tipos de Aristas (Edge Types)

| Tipo | Significado | Ejemplo |
|------|-------------|---------|
| `prerequisite` | Requiere conocimiento de | LFI → Path Traversal |
| `enables` | Permite realizar | Enumeration → Foothold |
| `implements` | Implementa concepto | RCE → Remote Code Execution |
| `references` | Cita/referencia | Article → CVE |
| `related_to` | Concepto relacionado | SQL Injection → XSS |
| `exploits` | Explota vulnerabilidad | Technique → Web Vulnerability |
| `leads_to` | Conduce a siguiente fase | Enumeration → Foothold |
| `part_of` | Parte de procedimiento | Step1 → Attack Chain |
| `depends_on` | Depende de | Privilege Escalation → Foothold |

## Metadata Extendida (Optional)

Para chunks de HTB/CTF, se puede agregar metadata de grafo sin modificar el frontmatter base:

```yaml
---
chunk_id: technique::web::lua-rce::sandbox-escape::001
domain: web
chunk_type: technique
confidence: high
---

graph_metadata:
  primary_nodes:
    - enumeration
    - web_security
  edges:
    - target_node: foothold
      edge_type: enables
      weight: 0.85
  tags:
    - HTB-related
    - RCE-technique
  attack_phase: initial_access
  htb_machine: FACTS
  cve_ids:
    - CVE-2025-XXXX
```

## Exportación de Formatos

### JSON
```json
{
  "nodes": [
    {
      "id": "enumeration",
      "type": "enumeration",
      "label": "Enumeration",
      "severity": "critical",
      "confidence": 1.0
    }
  ],
  "edges": [
    {
      "id": "enum_foothold",
      "source": "enumeration",
      "target": "foothold",
      "type": "leads_to",
      "weight": 0.9
    }
  ],
  "stats": {
    "total_nodes": 50,
    "total_edges": 120,
    "processed_chunks": 38
  }
}
```

### GraphML
Formato XML compatible con:
- Gephi (análisis visual)
- Cytoscape (bioinformática)
- Neo4j (base de datos de grafos)
- yEd (editores de grafos)

## Estadísticas y Monitoreo

```python
# Via Python
stats = builder.get_stats()
print(f"Nodes: {stats['total_nodes']}")
print(f"Edges: {stats['total_edges']}")
print(f"Chunks: {stats['processed_chunks']}")

# Via API
curl http://localhost:8001/api/graph/stats
# Response:
# {
#   "total_nodes": 50,
#   "total_edges": 120,
#   "processed_chunks": 38
# }
```

## Próximas Fases

### Phase 2: Visualization (Próximas semanas)
- D3.js o Cytoscape.js frontend
- HTML rendering interactivo
- Filtrado de nodos por tipo
- Búsqueda y navegación
- Zoom y pan
- Export a PNG/SVG

### Phase 3: Advanced Features (2+ semanas)
- Neo4j integration para persistencia
- Pattern matching queries
- Graph algorithms (centrality, clustering)
- Recommendation engine
- Custom node/edge properties
- Graph analytics dashboard

## Troubleshooting

### Imports fallando
```bash
# Asegúrate de agregar al sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# O ejecutar desde directorio raíz
cd /home/kali/Desktop/RAG
python rag_graph/tests/smoke_tests.py
```

### Docker build fallando
```bash
# Limpia imágenes viejas
docker-compose down
docker rmi atlas-engine:local rag-graph:local

# Rebuild
docker-compose build
```

### API no responde
```bash
# Verifica que el servicio esté corriendo
docker-compose ps

# Revisa logs
docker-compose logs -f rag-graph

# Prueba conexión
curl http://localhost:8001/health
```

## Referências

- **txtai**: https://github.com/neuml/txtai
- **NetworkX**: https://networkx.org/
- **D3.js**: https://d3js.org/
- **Cytoscape.js**: http://js.cytoscape.org/
- **Neo4j**: https://neo4j.com/

## Contribuciones

Cualquier cambio a `rag_graph/` debe:
1. Pasar todos los tests: `pytest rag_graph/tests/ -v`
2. Pasar smoke tests: `python rag_graph/tests/smoke_tests.py`
3. Mantener compatibilidad con Docker Compose
4. Documentar cambios en commits
5. No afectar funcionalidad existente de RAG

## Licencia

Mismo que el proyecto RAG padre.

---

**Versión**: 1.0  
**Fecha**: Marzo 2026  
**Estado**: Rama `rag-graph` activa, Phase 1 completa  
**Próximo**: Phase 2 - Visualization
