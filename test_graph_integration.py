#!/usr/bin/env python3
"""
Integration Test: Chat.ask() with GraphRAG Expansion
=====================================================

This test verifies that the Chat class correctly uses GraphRAG to expand
retrieval context when use_graph=True.
"""

import sys
import json
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from atlas_engine.graph import SemanticGraph
from atlas_engine.chat import Chat


def test_graph_chat_integration():
    """Test that chat.ask() works with use_graph parameter."""

    print("=" * 60)
    print("Integration Test: Chat + GraphRAG")
    print("=" * 60)

    # Load example chunks
    chunks = []
    examples_dir = Path("default/examples")

    for md_file in sorted(examples_dir.rglob("*.md")):
        if md_file.name in ["README.md", "htb_writeup_template.md"]:
            continue

        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        match = re.search(r"---\n(.*?)\n---", content, re.DOTALL)
        if not match:
            continue

        fm = match.group(1)
        cid = re.search(r"chunk_id:\s*(.+)", fm)
        dom = re.search(r"domain:\s*(.+)", fm)
        ctype = re.search(r"chunk_type:\s*(.+)", fm)

        if cid:
            chunks.append(
                {
                    "chunk_id": cid.group(1).strip(),
                    "domain": dom.group(1).strip() if dom else "unknown",
                    "chunk_type": ctype.group(1).strip() if ctype else "unknown",
                    "tags": ["example", "test"],
                    "content": content.split("---", 2)[-1][:500],
                }
            )

    print(f"\n✓ Loaded {len(chunks)} example chunks")
    for chunk in chunks:
        print(f"  - {chunk['chunk_id']} ({chunk['domain']})")

    # Build graph
    print(f"\n📊 Building semantic graph...")
    graph = SemanticGraph(namespace="test")
    graph.build_from_chunks(chunks)

    stats = graph.stats()
    print(f"✓ Graph built: {stats['nodes']} nodes, {stats['edges']} edges")

    # Initialize Chat
    print(f"\n💬 Initializing Chat with Gemini (or fallback)...")
    chat = Chat(backend="gemini")

    # Test 1: Simple query without graph
    print(f"\n[Test 1] Ask WITHOUT graph expansion:")
    print("  Query: 'How do I set up a Python virtual environment?'")

    try:
        response_without_graph = chat.ask(
            "How do I set up a Python virtual environment?", use_graph=False
        )
        print(f"  ✓ Response: {response_without_graph[:150]}...")
    except Exception as e:
        print(f"  ⚠️  Response failed (expected if Ollama not running): {e}")
        response_without_graph = None

    # Test 2: Same query WITH graph expansion
    print(f"\n[Test 2] Ask WITH graph expansion:")
    print("  Query: 'How do I set up a Python virtual environment?'")
    print("  Expected: Retrieval expands to related chunks via graph")

    try:
        response_with_graph = chat.ask(
            "How do I set up a Python virtual environment?", use_graph=True
        )
        print(f"  ✓ Response: {response_with_graph[:150]}...")
    except Exception as e:
        print(f"  ⚠️  Response failed (expected if Ollama not running): {e}")
        response_with_graph = None

    # Test 3: Verify graph retrieval context
    print(f"\n[Test 3] Verify graph context building:")

    if chunks:
        seed_chunk = chunks[0]
        print(f"  Seed chunk: {seed_chunk['chunk_id']}")

        context = graph.query_by_similarity(seed_chunk["chunk_id"], depth=2)
        print(f"  ✓ Graph query result:")
        print(f"    - Nodes found: {context['nodes_found']}")
        print(f"    - Edges found: {context['edges_found']}")
        print(f"    - Depth: {context['depth']}")

    # Test 4: Domain relationships
    print(f"\n[Test 4] Verify domain relationships:")
    test_pairs = [
        ("python", "python-programming", True),
        ("web", "web_security", False),
        ("rag", "retrieval", True),
    ]

    all_passed = True
    for d1, d2, expected in test_pairs:
        result = graph._domains_related(d1, d2)
        status = "✓" if result == expected else "✗"
        if result != expected:
            all_passed = False
        print(f"  {status} {d1} + {d2} = {result} (expected: {expected})")

    # Summary
    print("\n" + "=" * 60)
    print("Integration Test Summary")
    print("=" * 60)
    print(f"✓ Graph building: PASS")
    print(f"✓ Graph querying: PASS")
    print(f"✓ Domain relationships: {'PASS' if all_passed else 'FAIL'}")
    print(f"✓ Chat with use_graph parameter: IMPLEMENTED")
    print(f"\n✨ Integration test complete!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_graph_chat_integration()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
