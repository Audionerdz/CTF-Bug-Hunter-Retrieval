# RAG-Graph: Knowledge Visualization System

RAG-Graph is a knowledge visualization system that converts RAG chunks into an interactive relational graph, enabling visual exploration of knowledge across attack phases and security domains.

## Features

- **Graph Construction**: Automatically builds knowledge graph from markdown chunks
- **Topic Mapping**: Maps chunks to attack phases (enumeration, foothold, post-exploitation, privilege escalation)
- **Domain Organization**: Organizes knowledge by security domains (web, Linux, Python, RAG, etc.)
- **Multiple Formats**: Export to JSON, GraphML, and interactive HTML
- **REST API**: Query and manipulate the graph via REST endpoints
- **Semantic Relations**: Connect chunks based on semantic relationships

## Architecture

```
rag_graph/
├── models/              # Data models (Node, Edge, Metadata)
├── builders/            # Graph construction from chunks
├── visualization/       # HTML/D3.js rendering
├── api/                # REST API endpoints
├── storage/            # Graph persistence
└── tests/              # Unit and integration tests
```

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r rag_graph/requirements_rag_graph.txt

# Or with Docker
docker-compose -f docker-compose.rag-graph.yml up
```

### Building a Graph

```python
from pathlib import Path
from rag_graph.builders.graph_builder import GraphBuilder

# Create builder
builder = GraphBuilder(chunks_dir=Path("./default"))

# Build graph
builder.build_graph(include_core_topics=True)

# Save results
builder.save_to_json(Path("graph.json"))
builder.save_to_graphml(Path("graph.graphml"))

# Check stats
print(builder.get_stats())
```

### Using the REST API

```bash
# Start API server
python -m rag_graph.api.server

# Query endpoints
curl http://localhost:8001/api/graph
curl http://localhost:8001/api/node/enumeration/neighbors
curl http://localhost:8001/api/path/enumeration/privilege_escalation
```

## Node Types

### Attack Phase Nodes
- `enumeration` - Information gathering
- `foothold` - Initial access
- `post_exploitation` - Post-access actions
- `privilege_escalation` - Privilege elevation

### Knowledge Domain Nodes
- `rag` - RAG methodology
- `python` - Python programming
- `web_security` - Web vulnerabilities
- `linux_security` - Linux exploitation
- `windows_security` - Windows exploitation
- `networking` - Network concepts
- `cryptography` - Cryptographic concepts
- `reverse_engineering` - Binary analysis

### Content Nodes
- `chunk` - Individual knowledge chunk
- `technique` - Security technique
- `exploit` - Exploitation code
- `procedure` - Step-by-step procedure
- `guideline` - Best practices
- `reference` - Quick reference

## Edge Types

- `prerequisite` - Requires knowledge of
- `enables` - Allows performing
- `implements` - Implements concept
- `references` - Cites/references
- `related_to` - Related concept
- `exploits` - Exploits vulnerability
- `leads_to` - Leads to next phase
- `part_of` - Part of procedure

## Graph Metadata (Optional)

For HTB/CTF chunks, optional metadata can be added:

```yaml
---
chunk_id: technique::web::lua-rce::sandbox-escape::001
domain: web
chunk_type: technique
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
```

## Testing

```bash
# Run all tests
pytest rag_graph/tests/ -v

# Run with coverage
pytest rag_graph/tests/ --cov=rag_graph

# Run specific test
pytest rag_graph/tests/test_models.py::TestNode -v
```

## Smoke Tests (CI/CD)

```bash
# Run Docker smoke tests
docker-compose -f docker-compose.rag-graph.yml run --rm rag-graph pytest rag_graph/tests/ -v

# Check API health
curl http://localhost:8001/health
```

## Integration with Existing RAG

- **No modifications to chunks**: Existing chunks remain unchanged
- **Non-invasive metadata**: Optional graph metadata doesn't affect chunk parsing
- **Shared Docker Compose**: Runs alongside main atlas service
- **Read-only access**: Graph builder only reads from `default/`

## Export Formats

### JSON
```json
{
  "nodes": [...],
  "edges": [...],
  "stats": {
    "total_nodes": 50,
    "total_edges": 120
  }
}
```

### GraphML
Compatible with:
- Gephi
- Cytoscape
- Neo4j
- yEd

### HTML/D3.js (Coming Soon)
Interactive visualization with:
- Node filtering
- Edge highlighting
- Zoom/pan
- Custom styling

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/graph` | Get complete graph |
| GET | `/api/graph/nodes` | List all nodes |
| GET | `/api/graph/edges` | List all edges |
| GET | `/api/node/{id}` | Get specific node |
| GET | `/api/node/{id}/neighbors` | Get neighbors of node |
| GET | `/api/path/{from}/{to}` | Calculate path between nodes |
| POST | `/api/graph/rebuild` | Rebuild graph from chunks |
| GET | `/health` | Health check |

## Development

### Running Tests
```bash
pytest rag_graph/tests/ -v --cov=rag_graph
```

### Code Quality
```bash
# Format code
black rag_graph/

# Check lint
flake8 rag_graph/

# Type checking
mypy rag_graph/
```

## Known Limitations

- **Phase 1**: Basic graph construction and JSON export
- **Visualization**: Coming in Phase 2
- **Neo4j**: Optional, planned for Phase 3
- **Advanced Querying**: Pattern matching planned

## Roadmap

### Phase 1 (Current)
- [x] Core data models (Node, Edge)
- [x] GraphBuilder from chunks
- [x] JSON/GraphML export
- [ ] Basic REST API
- [ ] Docker integration
- [ ] Smoke tests

### Phase 2
- [ ] Interactive D3.js visualization
- [ ] HTML rendering
- [ ] Advanced filtering

### Phase 3
- [ ] Neo4j integration
- [ ] Pattern matching queries
- [ ] Graph analytics (centrality, clustering)
- [ ] Recommendation engine

## Contributing

This project is part of the RAG knowledge system. See main RAG repository for contribution guidelines.

## References

- **txtai**: https://github.com/neuml/txtai
- **NetworkX**: https://networkx.org/
- **D3.js**: https://d3js.org/
- **Neo4j**: https://neo4j.com/

## License

Same as parent RAG project.

---

**Version**: 0.1.0  
**Status**: Early Development (Phase 1)  
**Last Updated**: 2026-03-01
