# Contributing to Elementum DSA Framework

Thank you for your interest in contributing to the Elementum Domain-Specific Agent (DSA) Governance Framework. This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

All contributors are expected to adhere to the project's code of conduct. Please be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/elementum-dsa-project.git`
3. Create a branch for your changes: `git checkout -b feature/your-feature-name`
4. Install development dependencies: `pip install -e ".[dev]"`

## Development Process

### Setting Up the Development Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Running Tests

```bash
pytest tests/
```

### Code Style

We follow PEP 8 style guidelines. Use the following tools to ensure your code meets the style requirements:

```bash
# Format code
black .

# Sort imports
isort .

# Check typing
mypy .

# Lint code
flake8 .
```

## Adding a New Agent

1. Copy the appropriate template from `/agents/templates`
2. Implement the required interfaces
3. Create a corresponding knowledge base
4. Add tests for your implementation
5. Update documentation

## Adding a New Knowledge Base

1. Copy the appropriate template from `/knowledge/templates`
2. Implement the required knowledge components
3. Validate against the schema in `/knowledge/schemas`
4. Add tests for your implementation
5. Update documentation

## Pull Request Process

1. Update the README.md or documentation with details of changes if appropriate
2. Run tests to ensure your changes don't break existing functionality
3. Ensure your code meets style guidelines
4. Submit a pull request with a clear description of the changes

## Versioning

We use semantic versioning (SemVer) for version management:

- Major version (X.0.0): Incompatible API changes
- Minor version (X.Y.0): Backwards-compatible functionality additions
- Patch version (X.Y.Z): Backwards-compatible bug fixes

## License

By contributing, you agree that your contributions will be licensed under the project's license.