"""
Integration tests for GraphBuilder

Tests building graphs from actual chunk files.
"""

import pytest
from pathlib import Path
import tempfile
import json
from rag_graph.builders.graph_builder import GraphBuilder
from rag_graph.models.node import NodeType


class TestGraphBuilder:
    """Tests for GraphBuilder functionality"""

    @pytest.fixture
    def temp_chunks_dir(self):
        """Create a temporary chunks directory with sample chunks"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Create sample chunk structure
            web_dir = tmpdir / "web" / "lua-rce"
            web_dir.mkdir(parents=True)

            # Create sample chunk file
            chunk_file = web_dir / "sandbox-escape_001.md"
            chunk_content = """---
chunk_id: technique::web::lua-rce::sandbox-escape::001
domain: web
chunk_type: technique
confidence: high
source: example
creator: test
---

# Lua RCE Sandbox Escape Technique

This is a sample technique chunk for testing the graph builder.

## Overview
Demonstrates how to escape Lua sandboxes for remote code execution.

## Exploitation Steps
1. Identify sandbox environment
2. Find escape vectors
3. Execute arbitrary code
"""
            chunk_file.write_text(chunk_content)

            yield tmpdir

    def test_graph_builder_init(self):
        """Test GraphBuilder initialization"""
        builder = GraphBuilder()
        assert builder.nodes.count() == 0
        assert builder.edges.count() == 0

    def test_create_core_topics(self, temp_chunks_dir):
        """Test creating core topic nodes"""
        builder = GraphBuilder(chunks_dir=temp_chunks_dir)
        builder._create_core_topic_nodes()

        # Should have 4 attack phases + 8 knowledge domains
        assert builder.nodes.count() == 12

        # Check attack phase nodes exist
        assert builder.nodes.get("enumeration") is not None
        assert builder.nodes.get("foothold") is not None
        assert builder.nodes.get("post_exploitation") is not None
        assert builder.nodes.get("privilege_escalation") is not None

        # Check knowledge domain nodes exist
        assert builder.nodes.get("rag") is not None
        assert builder.nodes.get("python") is not None
        assert builder.nodes.get("web_security") is not None

    def test_phase_sequence_edges(self, temp_chunks_dir):
        """Test that phase nodes are connected in sequence"""
        builder = GraphBuilder(chunks_dir=temp_chunks_dir)
        builder._create_core_topic_nodes()

        # Should have edges connecting phases
        assert builder.edges.count() == 3  # 4 phases = 3 edges

        # Check specific edges
        enum_to_foothold = False
        for edge in builder.edges.edges.values():
            if edge.source_id == "enumeration" and edge.target_id == "foothold":
                enum_to_foothold = True
                break

        assert enum_to_foothold, "Enumeration should lead to Foothold"

    def test_process_chunk(self, temp_chunks_dir):
        """Test processing a single chunk"""
        builder = GraphBuilder(chunks_dir=temp_chunks_dir)

        chunk_file = list(temp_chunks_dir.rglob("*.md"))[0]
        node = builder._process_chunk(chunk_file)

        assert node is not None
        assert node.node_id == "technique::web::lua-rce::sandbox-escape::001"
        assert node.source_path == str(chunk_file)

    def test_full_graph_build(self, temp_chunks_dir):
        """Test building a complete graph"""
        builder = GraphBuilder(chunks_dir=temp_chunks_dir)
        success = builder.build_graph(include_core_topics=True)

        assert success is True

        # Should have core topics + at least one chunk node
        assert builder.nodes.count() >= 13  # 12 core + 1 chunk
        assert builder.edges.count() >= 3  # At least phase sequence edges

    def test_save_to_json(self, temp_chunks_dir):
        """Test saving graph to JSON"""
        builder = GraphBuilder(chunks_dir=temp_chunks_dir)
        builder.build_graph()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json_path = Path(f.name)

        try:
            success = builder.save_to_json(json_path)
            assert success is True

            # Verify JSON is valid
            with open(json_path) as f:
                data = json.load(f)

            assert "nodes" in data
            assert "edges" in data
            assert "stats" in data
            assert len(data["nodes"]) > 0
            assert len(data["edges"]) > 0

        finally:
            json_path.unlink()

    def test_save_to_graphml(self, temp_chunks_dir):
        """Test saving graph to GraphML"""
        builder = GraphBuilder(chunks_dir=temp_chunks_dir)
        builder.build_graph()

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".graphml", delete=False
        ) as f:
            graphml_path = Path(f.name)

        try:
            success = builder.save_to_graphml(graphml_path)
            assert success is True

            # Verify GraphML file exists and has content
            assert graphml_path.exists()
            content = graphml_path.read_text()
            assert "<?xml" in content
            assert "<graphml" in content
            assert "<graph" in content

        finally:
            graphml_path.unlink()

    def test_get_stats(self, temp_chunks_dir):
        """Test getting graph statistics"""
        builder = GraphBuilder(chunks_dir=temp_chunks_dir)
        builder.build_graph()

        stats = builder.get_stats()
        assert "total_nodes" in stats
        assert "total_edges" in stats
        assert "processed_chunks" in stats
        assert stats["total_nodes"] > 0
        assert stats["total_edges"] > 0


class TestGraphBuilderWithRealChunks:
    """Integration tests with actual RAG chunks if available"""

    @pytest.fixture
    def real_chunks_dir(self):
        """Get real chunks directory if it exists"""
        chunks_dir = Path(__file__).parent.parent.parent / "default"
        if chunks_dir.exists():
            return chunks_dir
        return None

    def test_build_with_real_chunks(self, real_chunks_dir):
        """Test building graph with real chunks"""
        if real_chunks_dir is None:
            pytest.skip("Real chunks directory not found")

        builder = GraphBuilder(chunks_dir=real_chunks_dir)
        success = builder.build_graph()

        assert success is True
        assert builder.nodes.count() > 12  # Core topics + some chunks
        assert builder.edges.count() > 3  # At least phase sequence edges

    def test_real_chunks_domain_mapping(self, real_chunks_dir):
        """Test that chunks are mapped to correct domains"""
        if real_chunks_dir is None:
            pytest.skip("Real chunks directory not found")

        builder = GraphBuilder(chunks_dir=real_chunks_dir)
        builder.build_graph()

        # Check that web_security domain node has connections
        web_security_outgoing = builder.edges.get_by_target("web_security")
        assert len(web_security_outgoing) > 0, (
            "Web security domain should have chunk connections"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
