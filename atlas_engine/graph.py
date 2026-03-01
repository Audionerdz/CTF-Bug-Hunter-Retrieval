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
    ):
        self.chunk_id = chunk_id
        self.domain = domain
        self.chunk_type = chunk_type
        self.tags = tags
        self.embedding = embedding
        self.content_preview = content_preview[:100]  # Truncate for preview


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
        if not self.graph:
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
        )

    def add_semantic_edge(
        self, chunk_id_a: str, chunk_id_b: str, weight: float
    ) -> None:
        """Add similarity-based edge between two chunks."""
        if not self.graph:
            return
        self.graph.add_edge(
            chunk_id_a,
            chunk_id_b,
            weight=weight,
            edge_type="semantic",
        )

    def add_tag_overlap_edge(self, chunk_id_a: str, chunk_id_b: str) -> None:
        """Add edge if chunks share tags."""
        if not self.graph:
            return
        self.graph.add_edge(
            chunk_id_a,
            chunk_id_b,
            weight=0.5,
            edge_type="tag_overlap",
        )

    def add_domain_edge(self, chunk_id_a: str, chunk_id_b: str) -> None:
        """Add edge if chunks share domain."""
        if not self.graph:
            return
        self.graph.add_edge(
            chunk_id_a,
            chunk_id_b,
            weight=0.3,
            edge_type="domain_affinity",
        )

    def build_from_chunks(
        self,
        chunks: List[Dict],
        embeddings: Optional[Dict[str, List[float]]] = None,
    ) -> None:
        """
        Build graph from list of chunk dicts.
        chunks: [{"chunk_id": "...", "domain": "...", "chunk_type": "...", "tags": [...], ...}]
        embeddings: {chunk_id: [float, ...]}
        """
        if not self.graph:
            raise RuntimeError("NetworkX not installed")

        # Add all nodes
        for chunk in chunks:
            chunk_id = chunk.get("chunk_id", "")
            if not chunk_id:
                continue
            emb = embeddings.get(chunk_id) if embeddings else None
            node = GraphNode(
                chunk_id=chunk_id,
                domain=chunk.get("domain", "unknown"),
                chunk_type=chunk.get("chunk_type", "unknown"),
                tags=chunk.get("tags", []),
                embedding=emb,
                content_preview=chunk.get("content", "")[:100],
            )
            self.add_node(node)

        # Add edges based on similarity, tags, domain
        chunk_ids = [c.get("chunk_id") for c in chunks if c.get("chunk_id")]

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

                # Domain affinity
                if self.nodes[id_a].domain == self.nodes[id_b].domain:
                    self.add_domain_edge(id_a, id_b)

    def query_by_similarity(self, seed_chunk_id: str, depth: int = 1) -> Dict[str, any]:
        """
        Expand from a seed chunk via BFS up to depth hops.
        Returns subgraph context.
        """
        if not self.graph:
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

        if not self.graph:
            return "Graph not initialized"

        net = Network(directed=False, notebook=False, height="750px", width="100%")
        net.from_nx(self.graph)
        net.show(output_path)
        return str(Path(output_path).resolve())

    def stats(self) -> Dict:
        """Get graph statistics."""
        if not self.graph:
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
