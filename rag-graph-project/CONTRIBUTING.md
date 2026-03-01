# Contributing to RAG-Graph

## Getting Started

### Prerequisites

- Python 3.9+
- pip or conda
- Git

### Setup Development Environment

```bash
# Clone and navigate
cd rag-graph-project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r rag_graph/requirements_rag_graph.txt
pip install black flake8 mypy pytest-cov
```

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Follow existing code style
- Add tests for new functionality
- Update docstrings

### 3. Run Tests

```bash
# Smoke tests
python rag_graph/tests/smoke_tests.py

# Unit tests
pytest rag_graph/tests/test_models.py -v

# Integration tests
pytest rag_graph/tests/test_graph_builder.py -v

# All tests with coverage
pytest rag_graph/tests/ --cov=rag_graph --cov-report=html
```

### 4. Code Quality

```bash
# Format with black
black rag_graph/

# Lint with flake8
flake8 rag_graph/

# Type check
mypy rag_graph/ --ignore-missing-imports
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: description of changes"
git push origin feature/your-feature-name
```

### 6. Create Pull Request

Push to GitHub and create PR with:
- Clear description
- Reference to issues (if any)
- Test results
- Screenshots/examples (if applicable)

## Code Style

### Python

- Follow PEP 8
- Max line length: 100 characters
- Use type hints where possible
- Add docstrings to classes/functions

### Example

```python
def my_function(param: str) -> bool:
    """
    Brief description.
    
    Args:
        param: Parameter description
    
    Returns:
        Result description
    """
    return True
```

## Testing Requirements

- All new features must have tests
- Minimum 80% code coverage
- Tests must pass locally before PR
- Smoke tests must pass in CI/CD

### Test File Structure

```python
class TestFeatureName:
    def test_basic_functionality(self):
        """Test basic behavior"""
        pass
    
    def test_edge_cases(self):
        """Test edge cases"""
        pass
    
    def test_error_handling(self):
        """Test error conditions"""
        pass
```

## Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation
- **refactor**: Code refactoring
- **test**: Adding tests
- **perf**: Performance improvement
- **chore**: Build/dependency changes

### Example

```
feat: add pattern matching to graph queries

- Implement basic pattern matching
- Add tests for pattern matching
- Update API documentation

Closes #123
```

## Reporting Issues

### Bug Report

```markdown
**Description**: Brief description
**Steps to Reproduce**: 
1. Step one
2. Step two
**Expected**: What should happen
**Actual**: What actually happened
**Environment**: Python version, OS, etc.
```

### Feature Request

```markdown
**Description**: What you want to add
**Motivation**: Why you need this
**Proposed Solution**: How to implement
**Alternatives**: Other approaches considered
```

## Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add examples for new features
- Keep CHANGELOG updated

## Release Process

### Version Numbering

Use semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features
- **PATCH**: Bug fixes

### Steps

1. Update version in `__init__.py`
2. Update CHANGELOG.md
3. Create git tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`

## Review Process

- Minimum 1 approval required
- All tests must pass
- Code quality checks must pass
- Documentation must be updated

## Questions?

- Check existing documentation
- Review similar implementations
- Ask in GitHub discussions
- Open an issue if blocked

## Code of Conduct

- Be respectful
- Focus on code, not person
- Help others learn
- Report violations

---

Thank you for contributing! Your efforts help make RAG-Graph better.
