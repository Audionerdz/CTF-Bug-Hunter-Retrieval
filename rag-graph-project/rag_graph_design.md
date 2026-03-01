# RAG-Graph Design Document

## Overview
RAG-Graph es un sistema de visualización de conocimiento que convierte chunks de RAG en un grafo relacional con nodos temáticos y conexiones semánticas. Basado en la metodología de txtai pero optimizado para CTF y ofensiva.

## Arquitectura

### 1. Modelo de Datos

#### Node Types (Nodos)
```
CORE_TOPIC_NODES:
  - enumeration      (Descubrimiento de información)
  - foothold         (Obtener acceso inicial)
  - post_exploitation (Acciones post-acceso)
  - privilege_escalation (Escalada de privilegios)

KNOWLEDGE_DOMAIN_NODES:
  - rag              (RAG methodology)
  - python           (Programming knowledge)
  - web_security     (Web vulnerabilities)
  - linux_security   (Linux exploitation)
  - networking       (Network concepts)

CHUNK_NODES:
  - Cada chunk se convierte en un nodo con metadata
```

#### Edge Types (Relaciones)
```
SEMANTIC_EDGES:
  - prerequisite     (requiere conocimiento de)
  - enables          (permite realizar)
  - references       (cita a)
  - related_to       (relacionado con)
  - implements       (implementa concepto)
  - exploits         (explota vulnerabilidad en)

ATTACK_CHAIN_EDGES:
  - leads_to         (conduce a siguiente fase)
  - part_of          (parte de procedimiento)
```

### 2. Estructura de Directorios

```
/rag_graph/                           [AISLADO]
├── README.md                         # Documentación del módulo
├── __init__.py                       # Package initialization
├── models/
│   ├── __init__.py
│   ├── node.py                       # Node data classes
│   ├── edge.py                       # Edge data classes
│   └── metadata.py                   # Metadata structures
├── builders/
│   ├── __init__.py
│   ├── graph_builder.py              # Construye grafo desde chunks
│   ├── chunk_processor.py            # Procesa chunks existentes
│   └── relation_extractor.py         # Extrae relaciones
├── visualization/
│   ├── __init__.py
│   ├── renderer.py                   # Renderiza grafo (HTML/D3.js)
│   └── graph_export.py               # Exporta a múltiples formatos
├── api/
│   ├── __init__.py
│   ├── server.py                     # FastAPI REST server
│   └── routes.py                     # API endpoints
├── storage/
│   ├── __init__.py
│   ├── graph_db.py                   # Neo4j/GraphML storage
│   └── metadata_store.py             # Metadata persistence
├── tests/
│   ├── __init__.py
│   ├── test_graph_builder.py
│   ├── test_visualization.py
│   ├── test_api.py
│   └── test_integration.py
├── examples/
│   ├── build_graph_example.py
│   ├── visualize_example.py
│   └── query_example.py
├── Dockerfile.rag-graph              # Dockerfile aislado
├── docker-compose.rag-graph.yml      # Docker compose para RAG-Graph
└── requirements_rag_graph.txt        # Dependencias aisladas
```

### 3. Metadata Schema para Chunks

#### Extensión del Frontmatter (sin modificar existente)
```yaml
---
chunk_id: technique::web::lua-rce::sandbox-escape::001
domain: web
chunk_type: technique
confidence: medium
reuse_level: universal
source: youtube
creator: freeCodeCamp
---

# NUEVA METADATA (si es chunk HTB/CTF)
graph_metadata:
  nodes:
    - name: "enumeration"
      relevance: 0.9
    - name: "web_security"
      relevance: 0.8
  edges:
    - target_node: "foothold"
      edge_type: "enables"
      weight: 0.85
    - target_node: "lua-sandbox-escape"
      edge_type: "implements"
      weight: 0.9
  tags:
    - "HTB-related"
    - "RCE-technique"
  attack_phase: "initial_access"
```

### 4. Componentes Principales

#### 4.1 GraphBuilder
```python
class GraphBuilder:
    def build_from_chunks(self, chunks_dir):
        """Construye grafo desde carpeta default/"""
        pass
    
    def add_chunk_node(self, chunk_path):
        """Añade chunk como nodo al grafo"""
        pass
    
    def extract_relations(self, chunk):
        """Extrae relaciones del contenido del chunk"""
        pass
    
    def connect_to_topics(self, chunk_node):
        """Conecta chunk a nodos temáticos"""
        pass
```

#### 4.2 Visualization
```python
class GraphRenderer:
    def render_html(self, graph):
        """Renderiza D3.js/Cytoscape.js HTML interactivo"""
        pass
    
    def export_graphml(self, graph):
        """Exporta a GraphML para herramientas externas"""
        pass
    
    def export_json(self, graph):
        """Exporta JSON para consumo por frontend"""
        pass
```

#### 4.3 API REST
```
GET  /api/graph                    # Obtiene grafo completo
GET  /api/graph/nodes              # Lista todos los nodos
GET  /api/graph/edges              # Lista todas las aristas
GET  /api/node/{node_id}           # Obtiene nodo específico
GET  /api/node/{node_id}/neighbors # Obtiene vecinos
GET  /api/path/{from}/{to}         # Calcula camino entre nodos
POST /api/graph/rebuild            # Reconstruye grafo
```

### 5. Tecnologías

| Componente | Tech Stack |
|-----------|-----------|
| **Backend** | FastAPI + Python 3.11 |
| **Graph Storage** | NetworkX (en memoria) + Neo4j (persistencia opcional) |
| **Visualization** | D3.js / Cytoscape.js |
| **Testing** | pytest + Docker Compose |
| **Containerization** | Docker |

### 6. Workflow de Integración

1. **Build Phase**: Leer chunks de `default/`
2. **Extraction Phase**: Extraer metadata y relaciones
3. **Graph Construction**: Crear nodos y aristas
4. **Storage Phase**: Guardar en GraphML + JSON
5. **Visualization Phase**: Renderizar HTML interactivo
6. **API Phase**: Exponer REST API

### 7. CI/CD Integration

```
Docker Compose existente:
  ✓ atlas service (sin cambios)
  + rag-graph service (nuevo)
  
Smoke Tests:
  - Test construction de grafo
  - Test API endpoints
  - Test visualization rendering
  - Test con chunks reales
```

### 8. Aislamiento vs Integración

**Aislado:**
- Código en directorio `/rag_graph/`
- Dependencias separadas en `requirements_rag_graph.txt`
- Dockerfile.rag-graph propio
- Tests independientes

**Integrado:**
- Lee chunks de `default/` (sin modificar)
- Metadata adicional opcional (no requiere cambios)
- API accessible desde same compose network
- Comparte Git history en rama rag-graph

## Fases de Implementación

### Phase 1: Core (Esta semana)
- [ ] Estructura de directorios
- [ ] Modelos (Node, Edge, Metadata)
- [ ] GraphBuilder básico
- [ ] Smoke tests

### Phase 2: Visualization (Próxima semana)
- [ ] Renderer HTML/D3.js
- [ ] Interactividad basic
- [ ] Exportadores (GraphML, JSON)

### Phase 3: API & Advanced (2 semanas)
- [ ] FastAPI server
- [ ] Endpoints REST
- [ ] Neo4j integration opcional
- [ ] Advanced querying

## Referencias
- txtai: https://github.com/neuml/txtai
- Cytoscape.js: http://js.cytoscape.org/
- Neo4j: https://neo4j.com/
- NetworkX: https://networkx.org/
