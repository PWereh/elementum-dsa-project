"""Unit tests for the Agent class.

Tests the base Agent class functionality.
"""

import pytest
from typing import Dict, Any, List
from core.agent import Agent


class TestAgent(Agent):
    """Test implementation of the Agent class."""

    def _initialize(self):
        """Initialize agent-specific resources."""
        self.initialized = True

    def process_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a user query.

        Args:
            query: The user query
            context: Optional context information

        Returns:
            Response dictionary with results
        """
        return {
            "agent_id": self.agent_id,
            "domain": self.domain,
            "query": query,
            "response": "Test response",
            "status": "complete"
        }

    def validate_response(self, response: Dict[str, Any]) -> bool:
        """Validate agent response.

        Args:
            response: The response to validate

        Returns:
            True if valid, False otherwise
        """
        return (
            "agent_id" in response and
            "domain" in response and
            "query" in response and
            "response" in response and
            "status" in response
        )


def test_agent_initialization():
    """Test agent initialization."""
    # Arrange
    agent_id = "test-agent"
    domain = "test-domain"
    version = 1.0
    capabilities = ["test-capability"]
    
    # Act
    agent = TestAgent(agent_id, domain, version, capabilities)
    
    # Assert
    assert agent.agent_id == agent_id
    assert agent.domain == domain
    assert agent.version == version
    assert agent.capabilities == capabilities
    assert agent.knowledge_id == f"Elementum-DSA-{domain.upper()}-KNOWLEDGE-V{version}"
    assert hasattr(agent, "initialized")
    assert agent.initialized is True


def test_agent_process_query():
    """Test agent query processing."""
    # Arrange
    agent = TestAgent("test-agent", "test-domain", 1.0, ["test-capability"])
    query = "Test query"
    
    # Act
    response = agent.process_query(query)
    
    # Assert
    assert response["agent_id"] == "test-agent"
    assert response["domain"] == "test-domain"
    assert response["query"] == query
    assert response["response"] == "Test response"
    assert response["status"] == "complete"


def test_agent_validate_response():
    """Test agent response validation."""
    # Arrange
    agent = TestAgent("test-agent", "test-domain", 1.0, ["test-capability"])
    valid_response = {
        "agent_id": "test-agent",
        "domain": "test-domain",
        "query": "Test query",
        "response": "Test response",
        "status": "complete"
    }
    invalid_response = {
        "agent_id": "test-agent",
        "domain": "test-domain"
    }
    
    # Act & Assert
    assert agent.validate_response(valid_response) is True
    assert agent.validate_response(invalid_response) is False


def test_agent_string_representation():
    """Test agent string representation."""
    # Arrange
    agent = TestAgent("test-agent", "test-domain", 1.0, ["test-capability"])
    
    # Act
    agent_str = str(agent)
    
    # Assert
    assert agent_str == "test-agent (v1.0) - test-domain"
