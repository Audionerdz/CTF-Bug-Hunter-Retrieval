"""
Example: Building and Visualizing a RAG Knowledge Graph

This script demonstrates how to:
1. Build a knowledge graph from RAG chunks
2. Export to different formats
3. Query the graph
"""

from pathlib import Path
import json
from rag_graph.builders.graph_builder import GraphBuilder


def main():
    """Main example function"""

    # Paths
    chunks_dir = Path(__file__).parent.parent.parent / "default"
    output_dir = Path(__file__).parent.parent.parent / "graph_exports"
    output_dir.mkdir(exist_ok=True)

    print("RAG-Graph Example: Build and Visualize")
    print("=" * 60)

    # Step 1: Initialize builder
    print("\n[Step 1] Initializing GraphBuilder...")
    builder = GraphBuilder(chunks_dir=chunks_dir)
    print(f"  Chunks directory: {chunks_dir}")

    # Step 2: Build graph
    print("\n[Step 2] Building knowledge graph...")
    success = builder.build_graph(include_core_topics=True)

    if not success:
        print("  ❌ Graph build failed")
        return False

    stats = builder.get_stats()
    print(f"  ✓ Graph built successfully")
    print(f"    - Nodes: {stats['total_nodes']}")
    print(f"    - Edges: {stats['total_edges']}")
    print(f"    - Chunks processed: {stats['processed_chunks']}")

    # Step 3: Export to JSON
    print("\n[Step 3] Exporting to JSON...")
    json_path = output_dir / "graph.json"
    if builder.save_to_json(json_path):
        print(f"  ✓ Saved to: {json_path}")

        # Show sample of JSON structure
        with open(json_path) as f:
            data = json.load(f)

        print(f"    - Contains {len(data['nodes'])} nodes")
        print(f"    - Contains {len(data['edges'])} edges")

        # Sample nodes
        print("\n  Sample nodes:")
        for node in data["nodes"][:3]:
            print(f"    - {node['label']} ({node['type']})")
    else:
        print("  ❌ JSON export failed")

    # Step 4: Export to GraphML
    print("\n[Step 4] Exporting to GraphML...")
    graphml_path = output_dir / "graph.graphml"
    if builder.save_to_graphml(graphml_path):
        print(f"  ✓ Saved to: {graphml_path}")
        print("    - Compatible with: Gephi, Cytoscape, Neo4j, yEd")
    else:
        print("  ❌ GraphML export failed")

    # Step 5: Query graph
    print("\n[Step 5] Querying the graph...")

    # Get enumeration node neighbors
    enum_neighbors = builder.edges.get_neighbors("enumeration")
    print(f"  - Enumeration node connections:")
    print(f"    - Outgoing edges: {len(enum_neighbors['outgoing'])}")
    print(f"    - Incoming edges: {len(enum_neighbors['incoming'])}")

    if enum_neighbors["outgoing"]:
        print(f"    - First outgoing edge leads to:")
        first_edge = enum_neighbors["outgoing"][0]
        target_node = builder.nodes.get(first_edge.target_id)
        if target_node:
            print(f"      {target_node.label}")

    # Get all nodes by type
    print(f"\n  - Nodes by type:")
    from rag_graph.models.node import NodeType

    for node_type in [NodeType.ENUMERATION, NodeType.FOOTHOLD, NodeType.RAG]:
        nodes_of_type = builder.nodes.get_by_type(node_type)
        print(f"    - {node_type.value}: {len(nodes_of_type)} node(s)")

    # Step 6: Statistics
    print("\n[Step 6] Graph Statistics")
    print(f"  - Total nodes: {stats['total_nodes']}")
    print(f"  - Total edges: {stats['total_edges']}")
    print(f"  - Chunks processed: {stats['processed_chunks']}")
    print(
        f"  - Average edges per node: {stats['total_edges'] / max(stats['total_nodes'], 1):.2f}"
    )

    print("\n" + "=" * 60)
    print("✓ Example completed successfully!")
    print(f"  Output files saved to: {output_dir}")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
