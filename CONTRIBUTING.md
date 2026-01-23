# Contributing to Cypher

First off, thank you for considering contributing to Cypher! It's people like you that make Cypher such a great tool.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct:
- Be respectful and inclusive
- Welcome newcomers
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, screenshots, etc.)
- **Describe the behavior you observed and what you expected**
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any alternatives you've considered**

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the development setup** instructions in README.md
3. **Make your changes** following our coding standards
4. **Add tests** if you're adding functionality
5. **Ensure all tests pass** (`pytest tests/`)
6. **Update documentation** if needed
7. **Write a clear commit message**
8. **Submit your pull request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/cypher.git
cd cypher

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your configuration

# Run tests
python -m pytest tests/ -v
```

## Coding Style

- **Python Code**: Follow [PEP 8](https://pep8.org/)
- **JavaScript**: Use modern ES6+ syntax
- **Comments**: Write clear, concise comments explaining "why", not "what"
- **Naming**: Use descriptive variable and function names
- **Functions**: Keep functions small and focused on one task

### Python Style Guide

```python
# Good
def calculate_gpa(subjects: List[Dict]) -> float:
    """Calculate GPA from subject grades."""
    # Implementation
    pass

# Avoid
def calc(s):
    pass
```

### JavaScript Style Guide

```javascript
// Good
async function fetchResults(formData) {
    // Clear purpose and error handling
    try {
        const response = await fetch(url, options);
        return await response.json();
    } catch (error) {
        handleError(error);
    }
}

// Avoid
function doStuff(d) {
    // Unclear purpose
}
```

## Testing

- Write unit tests for new functionality
- Ensure all existing tests pass
- Aim for high test coverage
- Test edge cases and error conditions

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/unit/test_validators.py -v

# Run with coverage
python -m pytest tests/ --cov=backend --cov-report=html
```

## Documentation

- Update README.md if you change functionality
- Add docstrings to new functions/classes
- Update API.md for API changes
- Add comments for complex logic

## Project Structure

```
cypher/
├── backend/          # Flask API
│   ├── services/    # Business logic
│   ├── core/        # Configuration
│   └── utils/       # Helpers
├── frontend/        # Web UI
├── tests/          # Test suite
│   ├── unit/       # Unit tests
│   ├── integration/# Integration tests
│   └── benchmarks/ # Performance tests
└── docs/           # Documentation
```

## Git Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line: brief summary (50 chars or less)
- Blank line, then detailed description if needed

```
Add input validation to API endpoints

- Implement hall ticket validation
- Add sanitization for user inputs
- Update error messages for clarity
```

## Review Process

1. **Automated Checks**: All PRs run automated tests
2. **Code Review**: At least one maintainer will review
3. **Feedback**: Address any requested changes
4. **Merge**: Once approved, maintainers will merge

## Getting Help

- **Issues**: Create a GitHub issue
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check docs/ folder

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Cypher! 🎉
