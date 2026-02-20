#!/usr/bin/env python3
"""
Query chunks from rag-canonical-v1-emb3large by chunk_id
Usage: python3 query_chunk.py <chunk_id>
"""

import os
import sys
from pinecone import Pinecone

def load_api_key():
    with open("/root/.openskills/env/pinecone.env") as f:
        for line in f:
            if "PINECONE_API_KEY=" in line:
                return line.split("=")[1].strip()
    return None

def query_chunk(chunk_id):
    api_key = load_api_key()
    if not api_key:
        print("❌ PINECONE_API_KEY not found")
        return
    
    pc = Pinecone(api_key=api_key)
    idx = pc.Index("rag-canonical-v1-emb3large")
    
    try:
        results = idx.fetch(ids=[chunk_id])
        
        if results and results.get('vectors'):
            chunk = results['vectors'].get(chunk_id)
            if chunk:
                print(f"\n✅ Chunk encontrado: {chunk_id}\n")
                print("=" * 70)
                
                metadata = chunk.get('metadata', {})
                
                # Print metadata
                print("METADATA:")
                for key, value in metadata.items():
                    if key == 'content':
                        continue  # Process content separately
                    print(f"  {key}: {value}")
                
                # Print content
                content = metadata.get('content', '')
                if content:
                    print(f"\nCONTENT ({len(content)} chars):")
                    print("-" * 70)
                    print(content)
                    print("-" * 70)
                else:
                    print("\n⚠️  NO CONTENT FOUND")
                
            else:
                print(f"❌ Chunk {chunk_id} not found")
        else:
            print(f"❌ No results found")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 query_chunk.py <chunk_id>")
        print("Example: python3 query_chunk.py technique::linux::compression::001")
        sys.exit(1)
    
    chunk_id = sys.argv[1]
    query_chunk(chunk_id)

