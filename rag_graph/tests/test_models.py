"""
Tests for RAG-Graph data models

Tests for Node, Edge, and related data structures.
"""

import pytest
from datetime import datetime
from rag_graph.models.node import Node, NodeType, NodeSeverity, NodeCollection
from rag_graph.models.edge import Edge, EdgeType, EdgeDirection, EdgeCollection
from rag_graph.models.metadata import ChunkMetadata


class TestNode:
    """Tests for Node model"""

    def test_node_creation(self):
        """Test creating a basic node"""
        node = Node(
            node_id="test_001",
            node_type=NodeType.CHUNK,
            label="Test Node",
        )
        assert node.node_id == "test_001"
        assert node.node_type == NodeType.CHUNK
        assert node.label == "Test Node"
        assert node.confidence == 1.0

    def test_node_validation(self):
        """Test node validation"""
        with pytest.raises(ValueError):
            Node(node_id="", node_type=NodeType.CHUNK, label="Test")

        with pytest.raises(ValueError):
            Node(node_id="test", node_type=NodeType.CHUNK, label="")

    def test_node_to_dict(self):
        """Test converting node to dictionary"""
        node = Node(
            node_id="test_001",
            node_type=NodeType.ENUMERATION,
            label="Test Node",
            description="Test description",
        )
        node_dict = node.to_dict()

        assert node_dict["id"] == "test_001"
        assert node_dict["type"] == "enumeration"
        assert node_dict["label"] == "Test Node"

    def test_node_from_dict(self):
        """Test creating node from dictionary"""
        data = {
            "id": "test_001",
            "type": "enumeration",
            "label": "Test Node",
            "description": "Test description",
        }
        node = Node.from_dict(data)

        assert node.node_id == "test_001"
        assert node.node_type == NodeType.ENUMERATION
        assert node.label == "Test Node"


class TestNodeCollection:
    """Tests for NodeCollection"""

    def test_add_node(self):
        """Test adding nodes to collection"""
        collection = NodeCollection()
        node = Node(node_id="test_001", node_type=NodeType.CHUNK, label="Test")

        collection.add(node)
        assert collection.count() == 1
        assert collection.get("test_001") == node

    def test_remove_node(self):
        """Test removing nodes from collection"""
        collection = NodeCollection()
        node = Node(node_id="test_001", node_type=NodeType.CHUNK, label="Test")

        collection.add(node)
        assert collection.count() == 1

        removed = collection.remove("test_001")
        assert removed is True
        assert collection.count() == 0

    def test_get_by_type(self):
        """Test getting nodes by type"""
        collection = NodeCollection()

        node1 = Node(node_id="enum_001", node_type=NodeType.ENUMERATION, label="Enum")
        node2 = Node(node_id="chunk_001", node_type=NodeType.CHUNK, label="Chunk")
        node3 = Node(node_id="enum_002", node_type=NodeType.ENUMERATION, label="Enum 2")

        collection.add(node1)
        collection.add(node2)
        collection.add(node3)

        enums = collection.get_by_type(NodeType.ENUMERATION)
        assert len(enums) == 2


class TestEdge:
    """Tests for Edge model"""

    def test_edge_creation(self):
        """Test creating a basic edge"""
        edge = Edge(
            edge_id="edge_001",
            source_id="node_1",
            target_id="node_2",
            edge_type=EdgeType.ENABLES,
        )
        assert edge.edge_id == "edge_001"
        assert edge.source_id == "node_1"
        assert edge.target_id == "node_2"
        assert edge.weight == 1.0

    def test_edge_validation(self):
        """Test edge validation"""
        with pytest.raises(ValueError):
            Edge(edge_id="", source_id="n1", target_id="n2", edge_type=EdgeType.ENABLES)

        with pytest.raises(ValueError):
            Edge(edge_id="e1", source_id="", target_id="n2", edge_type=EdgeType.ENABLES)

        with pytest.raises(ValueError):
            Edge(
                edge_id="e1",
                source_id="n1",
                target_id="n2",
                edge_type=EdgeType.ENABLES,
                weight=1.5,  # Invalid weight
            )

    def test_edge_to_dict(self):
        """Test converting edge to dictionary"""
        edge = Edge(
            edge_id="edge_001",
            source_id="node_1",
            target_id="node_2",
            edge_type=EdgeType.PREREQUISITE,
            label="requires",
            weight=0.8,
        )
        edge_dict = edge.to_dict()

        assert edge_dict["id"] == "edge_001"
        assert edge_dict["source"] == "node_1"
        assert edge_dict["target"] == "node_2"
        assert edge_dict["type"] == "prerequisite"
        assert edge_dict["weight"] == 0.8


class TestEdgeCollection:
    """Tests for EdgeCollection"""

    def test_add_edge(self):
        """Test adding edges to collection"""
        collection = EdgeCollection()
        edge = Edge(
            edge_id="edge_001",
            source_id="n1",
            target_id="n2",
            edge_type=EdgeType.ENABLES,
        )

        collection.add(edge)
        assert collection.count() == 1
        assert collection.get("edge_001") == edge

    def test_get_neighbors(self):
        """Test getting incoming and outgoing edges"""
        collection = EdgeCollection()

        edge1 = Edge(
            edge_id="e1", source_id="n1", target_id="n2", edge_type=EdgeType.ENABLES
        )
        edge2 = Edge(
            edge_id="e2", source_id="n2", target_id="n3", edge_type=EdgeType.LEADS_TO
        )
        edge3 = Edge(
            edge_id="e3",
            source_id="n0",
            target_id="n2",
            edge_type=EdgeType.PREREQUISITE,
        )

        collection.add(edge1)
        collection.add(edge2)
        collection.add(edge3)

        neighbors = collection.get_neighbors("n2")
        assert len(neighbors["outgoing"]) == 1  # edge2
        assert len(neighbors["incoming"]) == 2  # edge1, edge3


class TestChunkMetadata:
    """Tests for ChunkMetadata"""

    def test_metadata_from_yaml_dict(self):
        """Test creating metadata from YAML dictionary"""
        yaml_dict = {
            "chunk_id": "technique::web::lua-rce::sandbox-escape::001",
            "domain": "web",
            "chunk_type": "technique",
            "confidence": "high",
            "source": "youtube",
            "creator": "freeCodeCamp",
        }

        metadata = ChunkMetadata.from_yaml_dict(yaml_dict)
        assert metadata.chunk_id == "technique::web::lua-rce::sandbox-escape::001"
        assert metadata.domain == "web"
        assert metadata.chunk_type == "technique"
        assert metadata.confidence == "high"

    def test_metadata_to_dict(self):
        """Test converting metadata to dictionary"""
        metadata = ChunkMetadata(
            chunk_id="test::001",
            domain="web",
            chunk_type="exploit",
        )

        metadata_dict = metadata.to_dict()
        assert metadata_dict["chunk_id"] == "test::001"
        assert metadata_dict["domain"] == "web"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
