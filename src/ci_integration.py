#!/usr/bin/env python3
"""CI integration flow for Atlas core commands."""

import os
import time
from pathlib import Path

from atlas_engine import Atlas


def main():
    ci_namespace = os.getenv("ATLAS_CI_NAMESPACE", f"ci-{int(time.time())}")
    test_chunk_id = f"ci::test::workflow::{int(time.time())}"
    test_chunk_path = Path("/tmp/atlas_ci_test_chunk.md")

    atlas = Atlas()

    print("[1/7] ask(gpt): What is LFI?")
    answer_1, sources_1 = atlas.ask("What is LFI?", backend="gpt")
    print(f"  answer chars={len(answer_1)} sources={len(sources_1)}")

    print("[2/7] query: ffuf cheatsheet")
    results = atlas.query("ffuf cheatsheet", top_k=3, show=False)
    print(f"  query results={len(results)}")

    print("[3/7] ask(gpt) again: What is LFI?")
    answer_2, sources_2 = atlas.ask("What is LFI?", backend="gpt")
    print(f"  answer chars={len(answer_2)} sources={len(sources_2)}")

    print("[4/7] fetch existing chunk")
    fetched = atlas.fetch("technique::web::fuzzing::ffuf-cheatsheet::001")
    print(f"  fetch found={bool(fetched)}")

    print("[5/7] create + vectorize test chunk")
    test_chunk_path.write_text(
        """
---
chunk_id: PLACEHOLDER
domain: ci
chunk_type: note
tags:
  - ci
  - test
---

This is a CI test chunk for Atlas vectorization and cleanup.
It should be inserted into Pinecone and then deleted in the same workflow.
""".replace("PLACEHOLDER", test_chunk_id).strip()
        + "\n",
        encoding="utf-8",
    )
    vec_result = atlas.vectorize(str(test_chunk_path), namespace=ci_namespace)
    print(f"  upserted={vec_result.get('upserted', 0)} namespace={ci_namespace}")

    print("[6/7] delete test chunk")
    deleted = atlas.delete(test_chunk_id, namespace=ci_namespace)
    print(f"  deleted={deleted}")

    print("[7/7] done")

    if test_chunk_path.exists():
        test_chunk_path.unlink()

    if not isinstance(results, list):
        raise RuntimeError("Query did not return a list")
    if not deleted:
        raise RuntimeError("Delete test chunk failed")


if __name__ == "__main__":
    main()
