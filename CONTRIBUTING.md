# Contributing to RAG Framework

Thank you for your interest in contributing! This guide will help you get started.

## Getting Started

1. **Fork & Clone**
```bash
git clone https://github.com/your-username/RAG.git
cd RAG
```

2. **Set up environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configure API keys**
```bash
mkdir -p .env
echo "PINECONE_API_KEY=your_key" > .env/pinecone.env
echo "OPENAI_API_KEY=your_key" > .env/openai.env
```

## Development Workflow

### Creating a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-name
```

### Code Style
- Follow PEP 8 for Python
- Use type hints where possible
- Keep functions focused and testable
- Add docstrings to public methods

### Making Changes
1. Write your changes
2. Test thoroughly
3. Update documentation if needed
4. Commit with clear messages

### Commit Messages
```
feat: add metadata injection to vectorizer
fix: handle plain markdown without frontmatter
docs: update installation guide
chore: clean up temporary files
```

### Testing
```bash
python3 -m py_compile rag/*.py src/*.py
```

## Pull Request Process

1. **Before submitting:**
   - Verify all files compile: `python3 -m py_compile rag/*.py src/*.py`
   - Test your changes with: `python3 -c "from rag import RAG; r = RAG()"`
   - Update documentation if you added features
   - Keep commits clean and meaningful

2. **PR Description:**
   - Explain what you changed and why
   - Reference any related issues
   - Include usage examples for new features

3. **Review:**
   - Be responsive to feedback
   - Make requested changes in new commits (don't amend)
   - Once approved, your PR will be merged

## What to Contribute

### Good Contributions
- Bug fixes with test cases
- Feature enhancements (ask first if major)
- Documentation improvements
- Performance optimizations
- CLI improvements

### Before Starting
- Check existing issues to avoid duplicates
- For major features, open an issue first
- Ask questions - we're here to help!

## Code Organization

```
RAG/
├── rag/                  # Framework package
│   ├── core.py          # Main RAG orchestrator
│   ├── vectorizer.py    # Vectorization pipeline
│   ├── query.py         # Query engine
│   ├── chat.py          # Chat backends
│   ├── chunker.py       # PDF/text chunking
│   ├── telegram.py      # Telegram integration
│   ├── registry.py      # Chunk registry
│   └── __init__.py
├── src/                 # CLI scripts (thin wrappers)
├── mkdocs/             # Documentation
├── default/            # Knowledge base (chunks)
├── config.py           # Configuration
└── requirements.txt
```

## Documentation

- User docs live in `mkdocs/docs/`
- Update relevant `.md` files when changing features
- Build locally: `cd mkdocs && mkdocs serve`
- Keep examples simple and practical

## Questions?

- Open an issue for bugs
- Check existing issues for answers
- Ask in pull request discussions
- Be respectful and constructive

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Happy contributing! 🚀
