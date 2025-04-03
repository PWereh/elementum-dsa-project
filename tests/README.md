# Elementum DSA Test Suite

This directory contains test suites for the Elementum Domain-Specific Agent (DSA) Governance Framework.

## Test Structure

- `/unit` - Unit tests for individual components
- `/integration` - Integration tests for component interactions
- `/functional` - Functional tests for end-to-end scenarios
- `/performance` - Performance benchmarks

## Running Tests

To run all tests:

```bash
pytest
```

To run a specific test suite:

```bash
pytest tests/unit/
```

To generate a coverage report:

```bash
pytest --cov=elementum_dsa tests/
```

## Writing Tests

All tests should follow the standard pytest format:

```python
def test_agent_initialization():
    # Arrange
    domain = "test_domain"
    version = 1.0
    capabilities = ["test_capability"]
    
    # Act
    agent = TestAgent(domain, version, capabilities)
    
    # Assert
    assert agent.domain == domain
    assert agent.version == version
    assert "test_capability" in agent.capabilities
```

## Test Data

Test data is stored in the `/tests/data` directory. This includes:

- Sample knowledge bases
- Test queries
- Expected responses
- Benchmark datasets

## Mocking

For unit tests, use pytest fixtures and mocks to isolate components:

```python
@pytest.fixture
def mock_knowledge_base():
    return MockKnowledgeBase()

def test_agent_with_mock_knowledge(mock_knowledge_base):
    agent = TestAgent(mock_knowledge_base)
    # Test implementation
```
