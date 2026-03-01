"""
GraphBuilder: Constructs knowledge graph from chunks

This module handles building the knowledge graph by:
1. Reading chunks from the default/ directory
2. Creating nodes for chunks and topics
3. Extracting and creating edges/relationships
4. Managing the graph structure
"""

import logging
from pathlib import Path
from typing import Optional, List, Dict, Set
import json
from dataclasses import asdict

from rag_graph.models.node import Node, NodeType, NodeSeverity, NodeCollection
from rag_graph.models.edge import Edge, EdgeType, EdgeDirection, EdgeCollection
from rag_graph.models.metadata import ChunkMetadata, ChunkParser


logger = logging.getLogger(__name__)


class GraphBuilder:
    """Builds and maintains the RAG knowledge graph"""

    def __init__(self, chunks_dir: Optional[Path] = None):
        """
        Initialize GraphBuilder.

        Args:
            chunks_dir: Path to the chunks directory (default: parent/default/)
        """
        if chunks_dir is None:
            # Default to ../default/ relative to this module
            chunks_dir = Path(__file__).parent.parent.parent / "default"

        self.chunks_dir = Path(chunks_dir)
        self.nodes = NodeCollection()
        self.edges = EdgeCollection()

        # Track processed chunks to avoid duplicates
        self._processed_chunks: Set[str] = set()

        logger.info(f"GraphBuilder initialized with chunks_dir: {self.chunks_dir}")

    def build_graph(self, include_core_topics: bool = True) -> bool:
        """
        Build the complete knowledge graph.

        Args:
            include_core_topics: Whether to create core topic nodes

        Returns:
            True if build succeeded, False otherwise
        """
        try:
            logger.info("Starting graph build...")

            # Create core topic nodes if requested
            if include_core_topics:
                self._create_core_topic_nodes()

            # Process all chunks
            chunk_files = list(self.chunks_dir.rglob("*.md"))
            logger.info(f"Found {len(chunk_files)} chunk files")

            for chunk_file in chunk_files:
                self._process_chunk(chunk_file)

            logger.info(
                f"Graph build complete. Nodes: {self.nodes.count()}, Edges: {self.edges.count()}"
            )
            return True

        except Exception as e:
            logger.error(f"Error building graph: {e}", exc_info=True)
            return False

    def _create_core_topic_nodes(self) -> None:
        """Create core topic nodes for attack phases and knowledge domains"""

        # Attack phase nodes
        attack_phases = [
            ("enumeration", "Enumeration", "Information gathering and discovery"),
            ("foothold", "Foothold", "Initial access and system compromise"),
            (
                "post_exploitation",
                "Post Exploitation",
                "Post-access actions and data gathering",
            ),
            ("privilege_escalation", "Privilege Escalation", "Elevation of privileges"),
        ]

        for phase_id, label, desc in attack_phases:
            node = Node(
                node_id=phase_id,
                node_type=NodeType.ENUMERATION
                if phase_id == "enumeration"
                else NodeType(phase_id),
                label=label,
                description=desc,
                severity=NodeSeverity.CRITICAL,
                color="#FF6B6B",  # Red for attack phases
            )
            self.nodes.add(node)
            logger.debug(f"Added core topic node: {phase_id}")

        # Knowledge domain nodes
        domains = [
            ("rag", "RAG & NLP", "Retrieval-Augmented Generation knowledge"),
            ("python", "Python Programming", "Python programming concepts"),
            ("web_security", "Web Security", "Web application vulnerabilities"),
            ("linux_security", "Linux Security", "Linux exploitation techniques"),
            ("networking", "Networking", "Network protocols and attacks"),
            ("windows_security", "Windows Security", "Windows exploitation"),
            ("cryptography", "Cryptography", "Cryptographic concepts"),
            ("reverse_engineering", "Reverse Engineering", "Binary analysis"),
        ]

        for domain_id, label, desc in domains:
            node = Node(
                node_id=domain_id,
                node_type=NodeType(domain_id),
                label=label,
                description=desc,
                severity=NodeSeverity.HIGH,
                color="#4ECDC4",  # Teal for knowledge domains
            )
            self.nodes.add(node)
            logger.debug(f"Added knowledge domain node: {domain_id}")

        # Create edges between attack phases (sequential)
        phase_sequence = [
            "enumeration",
            "foothold",
            "post_exploitation",
            "privilege_escalation",
        ]
        for i in range(len(phase_sequence) - 1):
            source = phase_sequence[i]
            target = phase_sequence[i + 1]
            edge = Edge(
                edge_id=f"{source}_{target}_sequence",
                source_id=source,
                target_id=target,
                edge_type=EdgeType.LEADS_TO,
                label="leads to",
                weight=0.9,
                description="Natural progression in attack chain",
            )
            self.edges.add(edge)
            logger.debug(f"Added phase sequence edge: {source} -> {target}")

    def _process_chunk(self, chunk_path: Path) -> Optional[Node]:
        """
        Process a single chunk file and create corresponding node.

        Args:
            chunk_path: Path to the chunk markdown file

        Returns:
            Created Node or None if processing failed
        """
        try:
            # Parse chunk
            metadata, content = ChunkParser.parse_chunk(chunk_path)

            if metadata is None:
                logger.warning(f"Failed to parse chunk: {chunk_path}")
                return None

            # Check if already processed
            if metadata.chunk_id in self._processed_chunks:
                logger.debug(f"Chunk already processed: {metadata.chunk_id}")
                return None

            self._processed_chunks.add(metadata.chunk_id)

            # Create node for chunk
            node = Node(
                node_id=metadata.chunk_id,
                node_type=NodeType(metadata.chunk_type)
                if metadata.chunk_type in [t.value for t in NodeType]
                else NodeType.CHUNK,
                label=chunk_path.stem,  # Use filename as label
                description=content[:200] if content else None,
                confidence=self._parse_confidence(metadata.confidence),
                source_chunk_id=metadata.chunk_id,
                source_path=str(chunk_path),
                color="#95E1D3"
                if metadata.domain == "web"
                else "#F38181",  # Different colors per domain
            )

            self.nodes.add(node)
            logger.debug(f"Added chunk node: {metadata.chunk_id}")

            # Connect to knowledge domain if applicable
            self._connect_to_domain(node, metadata)

            return node

        except Exception as e:
            logger.error(f"Error processing chunk {chunk_path}: {e}")
            return None

    def _connect_to_domain(self, chunk_node: Node, metadata: ChunkMetadata) -> None:
        """Create edges connecting chunk to relevant knowledge domains"""

        # Map domain names to knowledge domain nodes
        domain_mapping = {
            "web": "web_security",
            "python": "python",
            "linux": "linux_security",
            "windows": "windows_security",
            "networking": "networking",
            "rag": "rag",
            "crypto": "cryptography",
            "reverse": "reverse_engineering",
        }

        domain_node_id = domain_mapping.get(metadata.domain)

        if domain_node_id and self.nodes.get(domain_node_id):
            edge = Edge(
                edge_id=f"{chunk_node.node_id}_belongs_to_{domain_node_id}",
                source_id=chunk_node.node_id,
                target_id=domain_node_id,
                edge_type=EdgeType.PART_OF,
                label="belongs to",
                weight=0.8,
                direction=EdgeDirection.DIRECTED,
            )
            self.edges.add(edge)
            logger.debug(
                f"Connected chunk {chunk_node.node_id} to domain {domain_node_id}"
            )

    def _parse_confidence(self, confidence_str: Optional[str]) -> float:
        """Convert confidence string to float value"""
        if confidence_str is None:
            return 1.0

        confidence_map = {
            "low": 0.3,
            "medium": 0.6,
            "high": 0.9,
            "critical": 1.0,
        }

        return confidence_map.get(confidence_str.lower(), 1.0)

    def save_to_json(self, output_path: Path) -> bool:
        """
        Save graph to JSON format.

        Args:
            output_path: Path to save JSON file

        Returns:
            True if successful, False otherwise
        """
        try:
            graph_data = {
                "nodes": self.nodes.to_list(),
                "edges": self.edges.to_list(),
                "stats": {
                    "total_nodes": self.nodes.count(),
                    "total_edges": self.edges.count(),
                },
            }

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(graph_data, f, indent=2, default=str)

            logger.info(f"Graph saved to JSON: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error saving graph to JSON: {e}")
            return False

    def save_to_graphml(self, output_path: Path) -> bool:
        """
        Save graph to GraphML format (compatible with Gephi, Cytoscape, etc).

        Args:
            output_path: Path to save GraphML file

        Returns:
            True if successful, False otherwise
        """
        try:
            # This is a simplified GraphML export
            # For full functionality, consider using networkx library
            graphml = self._generate_graphml()

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(graphml)

            logger.info(f"Graph saved to GraphML: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error saving graph to GraphML: {e}")
            return False

    def _generate_graphml(self) -> str:
        """Generate GraphML XML content"""

        graphml = """<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlnsn/graphml">
  <graph edgedefault="directed">
"""

        # Add nodes
        for node in self.nodes.nodes.values():
            graphml += f"""    <node id="{node.node_id}" label="{node.label}">
      <data key="type">{node.node_type.value}</data>
      <data key="description">{node.description or ""}</data>
    </node>
"""

        # Add edges
        for edge in self.edges.edges.values():
            graphml += f"""    <edge source="{edge.source_id}" target="{edge.target_id}" label="{edge.label or edge.edge_type.value}">
      <data key="type">{edge.edge_type.value}</data>
      <data key="weight">{edge.weight}</data>
    </edge>
"""

        graphml += """  </graph>
</graphml>"""

        return graphml

    def get_stats(self) -> Dict[str, int]:
        """Get graph statistics"""
        return {
            "total_nodes": self.nodes.count(),
            "total_edges": self.edges.count(),
            "processed_chunks": len(self._processed_chunks),
        }
