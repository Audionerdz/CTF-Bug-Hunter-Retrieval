#!/usr/bin/env python3
"""
Regenerate chunk_registry.json from all .md files in default/
"""

import json
from pathlib import Path

RAG_ROOT = Path("/home/kali/Desktop/RAG")
DEFAULT_DIR = RAG_ROOT / "default"
OUTPUT_FILE = RAG_ROOT / "chunk_registry.json"

registry = {}

# Walk through all .md files
for md_file in DEFAULT_DIR.rglob("*.md"):
    # Extract relative path for key generation
    rel_path = md_file.relative_to(DEFAULT_DIR)

    # Skip certain files
    if rel_path.name.startswith("_") or rel_path.name == "README.md":
        continue

    # Use relative path as key (without .md extension)
    # Example: linux/security/ssh-forensics-management_001.md
    # becomes: technique::linux::security::ssh-forensics-management::001

    parts = list(rel_path.parts[:-1])  # All dirs except the file
    filename = rel_path.stem  # Without .md

    # Parse filename to extract base name and number
    if "_" in filename:
        base_name, number = filename.rsplit("_", 1)
        chunks = parts + [base_name, number]
    else:
        chunks = parts + [filename, "001"]

    # Build chunk_id: technique::category::subcategory::name::number
    chunk_id = "technique::" + "::".join(chunks)
    registry[chunk_id] = str(md_file)

# Sort and save
sorted_registry = dict(sorted(registry.items()))
with open(OUTPUT_FILE, "w") as f:
    json.dump(sorted_registry, f, indent=2)

print(f"✅ Registry regenerated with {len(sorted_registry)} entries")
print(f"📁 File: {OUTPUT_FILE}")
