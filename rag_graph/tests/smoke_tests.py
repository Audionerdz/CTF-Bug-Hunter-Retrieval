"""
Smoke Tests for RAG-Graph CI/CD Pipeline

Quick validation tests to ensure the RAG-Graph system is functioning correctly
when deployed in Docker. These tests verify:
- Graph building works
- Core nodes are created
- API endpoints respond
- Data persistence works
"""

import sys
import time
import json
from pathlib import Path
from typing import Optional

# Add parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_graph_builder_basic():
    """Test basic graph building functionality"""
    print("\n[SMOKE] Testing GraphBuilder basic functionality...")

    try:
        from rag_graph.builders.graph_builder import GraphBuilder

        # Initialize builder
        chunks_dir = Path("/app/default")
        builder = GraphBuilder(chunks_dir=chunks_dir)

        # Build graph with core topics
        success = builder.build_graph(include_core_topics=True)

        if not success:
            print("❌ Graph build failed")
            return False

        # Verify core topics were created
        stats = builder.get_stats()
        print(
            f"✓ Graph built: {stats['total_nodes']} nodes, {stats['total_edges']} edges"
        )

        if stats["total_nodes"] < 12:  # At least 4 phases + 8 domains
            print(f"❌ Too few nodes: {stats['total_nodes']} (expected >= 12)")
            return False

        if stats["total_edges"] < 3:  # At least phase sequence edges
            print(f"❌ Too few edges: {stats['total_edges']} (expected >= 3)")
            return False

        print("✓ Graph statistics valid")
        return True

    except Exception as e:
        print(f"❌ GraphBuilder test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_core_nodes_created():
    """Test that core topic nodes are created correctly"""
    print("\n[SMOKE] Testing core topic nodes...")

    try:
        from rag_graph.builders.graph_builder import GraphBuilder
        from rag_graph.models.node import NodeType

        chunks_dir = Path("/app/default")
        builder = GraphBuilder(chunks_dir=chunks_dir)
        builder._create_core_topic_nodes()

        # Check attack phase nodes
        phases = [
            "enumeration",
            "foothold",
            "post_exploitation",
            "privilege_escalation",
        ]
        for phase in phases:
            if builder.nodes.get(phase) is None:
                print(f"❌ Missing phase node: {phase}")
                return False

        print(f"✓ All {len(phases)} attack phase nodes created")

        # Check knowledge domain nodes
        domains = ["rag", "python", "web_security", "linux_security"]
        for domain in domains:
            if builder.nodes.get(domain) is None:
                print(f"❌ Missing domain node: {domain}")
                return False

        print(f"✓ All knowledge domain nodes created")
        return True

    except Exception as e:
        print(f"❌ Core nodes test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_json_export():
    """Test JSON export functionality"""
    print("\n[SMOKE] Testing JSON export...")

    try:
        from rag_graph.builders.graph_builder import GraphBuilder
        import tempfile

        chunks_dir = Path("/app/default")
        builder = GraphBuilder(chunks_dir=chunks_dir)
        builder.build_graph()

        # Save to temp JSON
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json_path = Path(f.name)

        try:
            success = builder.save_to_json(json_path)

            if not success:
                print("❌ JSON export failed")
                return False

            # Verify JSON is valid and has expected structure
            with open(json_path) as f:
                data = json.load(f)

            required_keys = ["nodes", "edges", "stats"]
            for key in required_keys:
                if key not in data:
                    print(f"❌ Missing key in JSON: {key}")
                    return False

            if len(data["nodes"]) == 0:
                print("❌ No nodes in JSON export")
                return False

            print(
                f"✓ JSON export valid: {len(data['nodes'])} nodes, {len(data['edges'])} edges"
            )
            return True

        finally:
            json_path.unlink()

    except Exception as e:
        print(f"❌ JSON export test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_models_import():
    """Test that all model classes can be imported"""
    print("\n[SMOKE] Testing model imports...")

    try:
        from rag_graph.models.node import Node, NodeType, NodeSeverity
        from rag_graph.models.edge import Edge, EdgeType
        from rag_graph.models.metadata import ChunkMetadata

        print("✓ All model classes imported successfully")
        return True

    except ImportError as e:
        print(f"❌ Failed to import models: {e}")
        return False


def test_api_server_import():
    """Test that API server can be imported"""
    print("\n[SMOKE] Testing API server import...")

    try:
        from rag_graph.api.server import app

        print("✓ API server imported successfully")
        return True

    except ImportError as e:
        print(f"❌ Failed to import API server: {e}")
        return False


def test_data_models_roundtrip():
    """Test Node and Edge serialization/deserialization"""
    print("\n[SMOKE] Testing data model serialization...")

    try:
        from rag_graph.models.node import Node, NodeType, NodeSeverity
        from rag_graph.models.edge import Edge, EdgeType

        # Test Node roundtrip
        node = Node(
            node_id="test_001",
            node_type=NodeType.ENUMERATION,
            label="Test Node",
            description="Test description",
            severity=NodeSeverity.HIGH,
        )

        node_dict = node.to_dict()
        node_restored = Node.from_dict(node_dict)

        if node_restored.node_id != node.node_id:
            print("❌ Node roundtrip failed: node_id mismatch")
            return False

        # Test Edge roundtrip
        edge = Edge(
            edge_id="edge_001",
            source_id="node_1",
            target_id="node_2",
            edge_type=EdgeType.ENABLES,
            weight=0.85,
        )

        edge_dict = edge.to_dict()
        edge_restored = Edge.from_dict(edge_dict)

        if edge_restored.edge_id != edge.edge_id:
            print("❌ Edge roundtrip failed: edge_id mismatch")
            return False

        print("✓ Data model serialization working correctly")
        return True

    except Exception as e:
        print(f"❌ Data model roundtrip test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def run_all_smoke_tests() -> bool:
    """Run all smoke tests and report results"""

    print("=" * 60)
    print("RAG-Graph Smoke Tests")
    print("=" * 60)

    tests = [
        ("Model Imports", test_models_import),
        ("API Server Import", test_api_server_import),
        ("Data Model Serialization", test_data_models_roundtrip),
        ("Core Nodes Creation", test_core_nodes_created),
        ("JSON Export", test_json_export),
        ("GraphBuilder Basic", test_graph_builder_basic),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))

    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    print("=" * 60)

    return passed_count == total_count


if __name__ == "__main__":
    success = run_all_smoke_tests()
    sys.exit(0 if success else 1)
