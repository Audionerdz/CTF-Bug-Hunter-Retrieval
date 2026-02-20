#!/bin/bash
# 🚀 RAG System 3072D - Quick Start

echo "╔═════════════════════════════════════════════════════════════╗"
echo "║   RAG System 3072D - Quick Start                          ║"
echo "╚═════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Activate venv
echo -e "${BLUE}Activating virtual environment...${NC}"
source /root/.openskills/venv/bin/activate

echo ""
echo "✅ Environment ready!"
echo ""
echo -e "${GREEN}Available commands:${NC}"
echo ""
echo "1️⃣  Vectorize a machine:"
echo "   python3 /root/.openskills/vectorize_canonical_openai.py gavel"
echo ""
echo "2️⃣  Query the RAG:"
echo "   python3 /root/.openskills/query_canonical_openai.py 'RCE PHP'"
echo ""
echo "3️⃣  Query specific machine:"
echo "   python3 /root/.openskills/query_canonical_openai.py 'privesc' 5 gavel"
echo ""
echo "📚 Documentation:"
echo "   cat /root/.openskills/README_3072D_SETUP.md"
echo "   cat /root/.openskills/OFFICIAL_SCRIPTS.md"
echo ""
