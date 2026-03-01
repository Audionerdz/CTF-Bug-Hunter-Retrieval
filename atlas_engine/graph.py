"""
GraphRAG Module: Semantic Graph Construction & Traversal
=========================================================
Builds a knowledge graph from chunks with:
- Nodes: individual chunks (with semantic embeddings)
- Edges: semantic similarity, tag overlap, domain affinity
- Query: expand around seeds via graph traversal
- Export: interactive HTML (PyVis) for visualization
"""

import json
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Set

try:
    import networkx as nx
    from networkx import Graph
except ImportError:
    nx = None
    Graph = None

try:
    import numpy as np
except ImportError:
    np = None


class GraphNode:
    """Represents a chunk as a node in the knowledge graph."""

    def __init__(
        self,
        chunk_id: str,
        domain: str,
        chunk_type: str,
        tags: List[str],
        embedding: Optional[List[float]] = None,
        content_preview: str = "",
        machine: Optional[str] = None,
        htb: bool = False,
        vuln_types: Optional[List[str]] = None,
    ):
        self.chunk_id = chunk_id
        self.domain = domain
        self.chunk_type = chunk_type
        self.tags = tags
        self.embedding = embedding
        self.content_preview = content_preview[:100]
        self.machine = machine
        self.htb = htb
        self.vuln_types = vuln_types or []


class SemanticGraph:
    """
    Builds and traverses a semantic knowledge graph.
    Edges can be:
    - semantic: cosine similarity > threshold
    - tag_overlap: shared tags
    - domain_affinity: same domain
    - type_affinity: same chunk_type
    """

    def __init__(
        self,
        namespace: str = "root",
        similarity_threshold: float = 0.7,
        min_tag_overlap: int = 1,
    ):
        self.namespace = namespace
        self.similarity_threshold = similarity_threshold
        self.min_tag_overlap = min_tag_overlap
        self.graph = Graph() if Graph else None
        self.nodes: Dict[str, GraphNode] = {}
        self.embeddings: Dict[str, List[float]] = {}

    def add_node(self, node: GraphNode) -> None:
        """Add a chunk node to the graph."""
        if self.graph is None:
            raise RuntimeError("NetworkX not installed. Install: pip install networkx")
        self.nodes[node.chunk_id] = node
        if node.embedding:
            self.embeddings[node.chunk_id] = node.embedding
        self.graph.add_node(
            node.chunk_id,
            domain=node.domain,
            chunk_type=node.chunk_type,
            tags=node.tags,
            preview=node.content_preview,
            machine=node.machine,
            htb=node.htb,
            vuln_types=node.vuln_types,
        )

    def add_semantic_edge(
        self, chunk_id_a: str, chunk_id_b: str, weight: float
    ) -> None:
        """Add similarity-based edge between two chunks."""
        if self.graph is None:
            return
        self.graph.add_edge(
            chunk_id_a,
            chunk_id_b,
            weight=weight,
            edge_type="semantic",
        )

    def add_tag_overlap_edge(self, chunk_id_a: str, chunk_id_b: str) -> None:
        """Add edge if chunks share tags."""
        if self.graph is None:
            return
        self.graph.add_edge(
            chunk_id_a,
            chunk_id_b,
            weight=0.5,
            edge_type="tag_overlap",
        )

    def add_domain_edge(self, chunk_id_a: str, chunk_id_b: str) -> None:
        """Add edge if chunks share domain."""
        if self.graph is None:
            return
        self.graph.add_edge(
            chunk_id_a,
            chunk_id_b,
            weight=0.3,
            edge_type="domain_affinity",
        )

    def add_related_domain_edge(self, chunk_id_a: str, chunk_id_b: str) -> None:
        """Add edge if chunks have related domains (e.g., linux + linux_security)."""
        if self.graph is None:
            return
        self.graph.add_edge(
            chunk_id_a,
            chunk_id_b,
            weight=0.5,
            edge_type="domain_related",
        )

    def _domains_related(self, domain_a: str, domain_b: str) -> bool:
        """
        Check if two domains are semantically related.
        Returns True only for explicitly defined domain families.

        Examples:
        - python + python_programming -> True
        - python + python_security -> True (if exists)
        - web + web_security -> False (NOT related per requirements)
        - linux + linux_security -> True (if exists, but currently no such domains)
        - rag + retrieval -> True (both RAG-related)
        """
        if domain_a == domain_b:
            return False  # Already handled by add_domain_edge()

        # Define domain families that SHOULD be connected
        domain_families = {
            # Python family: connect python with python-related domains
            frozenset(["python", "python-programming"]): True,
            # RAG family: connect rag with related terminology
            frozenset(["rag", "retrieval"]): True,
            frozenset(["rag", "augment"]): True,
            # Network family: connect network with related domains
            frozenset(["network", "networking"]): True,
        }

        domain_pair = frozenset([domain_a.lower(), domain_b.lower()])

        for family, should_connect in domain_families.items():
            if domain_pair == family and should_connect:
                return True

        return False

    def build_from_chunks(
        self,
        chunks: List[Dict],
        embeddings: Optional[Dict[str, List[float]]] = None,
    ) -> None:
        """
        Build graph from list of chunk dicts.
        Supports both old (domain/chunk_type) and new (HTB) metadata.
        chunks: [{"chunk_id": "...", "domain": "...", "chunk_type": "...", "tags": [...], ...}]
        embeddings: {chunk_id: [float, ...]}
        """
        if self.graph is None:
            raise RuntimeError("NetworkX not installed")

        # Add all nodes
        for chunk in chunks:
            chunk_id = chunk.get("chunk_id", "")
            if not chunk_id:
                continue
            emb = embeddings.get(chunk_id) if embeddings else None

            # Extract vulnerability types from HTB metadata
            vuln_types = []
            for vuln in [
                "sqli",
                "xss",
                "lfi",
                "rce",
                "idor",
                "csrf",
                "ssrf",
                "ssti",
                "xxe",
            ]:
                if chunk.get(vuln, {}).get("present"):
                    vuln_types.append(vuln)

            # Detect RAG-related and LangChain-related chunks for special handling
            domain = chunk.get("domain", "unknown").lower()
            is_rag_topic = (
                "rag" in domain or "retrieval" in domain or "augment" in domain
            )
            is_langchain_topic = "langchain" in domain or "lc" in domain

            node = GraphNode(
                chunk_id=chunk_id,
                domain=chunk.get("domain", "unknown"),
                chunk_type=chunk.get("chunk_type", "unknown"),
                tags=chunk.get("tags", []),
                embedding=emb,
                content_preview=chunk.get("content", "")[:100],
                machine=chunk.get("machine", None),
                htb=chunk.get("htb", False),
                vuln_types=vuln_types,
            )
            self.add_node(node)

        # Add edges based on similarity, tags, domain
        chunk_ids = [c.get("chunk_id") for c in chunks if c.get("chunk_id")]

        # Track RAG and LangChain nodes for cluster edges
        rag_nodes = []
        langchain_nodes = []
        for i, cid in enumerate(chunk_ids):
            domain = chunks[i].get("domain", "").lower()
            if "rag" in domain or "retrieval" in domain or "augment" in domain:
                rag_nodes.append(cid)
            if "langchain" in domain or "lc" in domain:
                langchain_nodes.append(cid)

        for i, id_a in enumerate(chunk_ids):
            for id_b in chunk_ids[i + 1 :]:
                if id_a not in self.nodes or id_b not in self.nodes:
                    continue

                # Semantic similarity edge
                if embeddings and id_a in embeddings and id_b in embeddings and np:
                    emb_a = np.array(embeddings[id_a])
                    emb_b = np.array(embeddings[id_b])
                    similarity = float(np.dot(emb_a, emb_b)) / (
                        np.linalg.norm(emb_a) * np.linalg.norm(emb_b) + 1e-8
                    )
                    if similarity > self.similarity_threshold:
                        self.add_semantic_edge(id_a, id_b, weight=similarity)

                # Tag overlap
                tags_a = set(self.nodes[id_a].tags)
                tags_b = set(self.nodes[id_b].tags)
                if len(tags_a & tags_b) >= self.min_tag_overlap:
                    self.add_tag_overlap_edge(id_a, id_b)

                # Domain affinity (exact match)
                domain_a = self.nodes[id_a].domain.lower()
                domain_b = self.nodes[id_b].domain.lower()

                if domain_a == domain_b:
                    self.add_domain_edge(id_a, id_b)

                # Related domain edges (e.g., "linux" + "linux_security")
                if self._domains_related(domain_a, domain_b):
                    self.add_related_domain_edge(id_a, id_b)

                # RAG cluster edges (all RAG topics interconnected)
                if id_a in rag_nodes and id_b in rag_nodes:
                    self.graph.add_edge(id_a, id_b, weight=0.8, edge_type="rag_cluster")

                # LangChain cluster edges (all LangChain topics interconnected)
                if id_a in langchain_nodes and id_b in langchain_nodes:
                    self.graph.add_edge(
                        id_a, id_b, weight=0.8, edge_type="langchain_cluster"
                    )

    def query_by_similarity(self, seed_chunk_id: str, depth: int = 1) -> Dict[str, any]:
        """
        Expand from a seed chunk via BFS up to depth hops.
        Returns subgraph context.
        """
        if self.graph is None:
            raise RuntimeError("NetworkX not installed")
        if seed_chunk_id not in self.graph:
            return {"error": f"Chunk {seed_chunk_id} not found in graph"}

        visited = set()
        frontier = {seed_chunk_id}
        for _ in range(depth):
            new_frontier = set()
            for node_id in frontier:
                if node_id in visited:
                    continue
                visited.add(node_id)
                neighbors = list(self.graph.neighbors(node_id))
                new_frontier.update(neighbors)
            frontier = new_frontier

        subgraph = self.graph.subgraph(visited)
        return {
            "seed": seed_chunk_id,
            "depth": depth,
            "nodes_found": len(visited),
            "edges_found": subgraph.number_of_edges(),
            "node_ids": list(visited),
        }

    def export_html(self, output_path: str = "knowledge_graph.html") -> str:
        """
        Export graph as interactive HTML (PyVis).
        Returns path to saved HTML file.
        """
        try:
            from pyvis.network import Network
        except ImportError:
            return "PyVis not installed. Install: pip install pyvis"

        if self.graph is None:
            return "Graph not initialized"

        try:
            net = Network(directed=False, notebook=False, height="750px", width="100%")
            net.from_nx(self.graph)
            net.show(output_path)
        except Exception as e:
            # Fallback: write minimal HTML manually
            import json

            nodes = [{"id": node, "label": node} for node in self.graph.nodes()]
            edges = [{"from": u, "to": v} for u, v in self.graph.edges()]

            html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Knowledge Graph</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
    <style>
        html, body {{ height: 100%; margin: 0; padding: 0; }}
        #network {{ height: 100%; }}
    </style>
</head>
<body>
    <div id="network"></div>
    <script>
        var nodes = new vis.DataSet({json.dumps(nodes)});
        var edges = new vis.DataSet({json.dumps(edges)});
        var container = document.getElementById('network');
        var data = {{ nodes: nodes, edges: edges }};
        var options = {{}};
        var network = new vis.Network(container, data, options);
    </script>
</body>
</html>"""
            with open(output_path, "w") as f:
                f.write(html)

        return str(Path(output_path).resolve())

    def stats(self) -> Dict:
        """Get graph statistics."""
        if self.graph is None:
            return {"error": "Graph not initialized"}
        return {
            "namespace": self.namespace,
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
            "density": nx.density(self.graph) if nx else 0,
        }


def build_graph_from_registry(
    registry_path: str,
    namespace: str = "root",
    max_chunks: Optional[int] = None,
) -> Optional[SemanticGraph]:
    """
    Load chunk registry and build graph for a given namespace.
    registry_path: path to chunk_registry.json
    namespace: filter chunks by namespace
    """
    if not Path(registry_path).exists():
        print(f"Registry not found: {registry_path}")
        return None

    with open(registry_path) as f:
        registry = json.load(f)

    # Filter chunks by namespace
    chunks = [c for c in registry if c.get("namespace") == namespace]
    if max_chunks:
        chunks = chunks[:max_chunks]

    graph = SemanticGraph(namespace=namespace)
    graph.build_from_chunks(chunks, embeddings=None)  # No embeddings loaded
    return graph
