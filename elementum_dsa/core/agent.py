"""Base Agent Implementation

This module provides the base Agent class that all domain-specific agents must inherit from.
"""

from typing import List, Dict, Any
from abc import ABC, abstractmethod


class Agent(ABC):
    """Base Agent class for all domain-specific agents."""

    def __init__(self, agent_id: str, domain: str, version: float, capabilities: List[str]):
        """Initialize a new Agent instance.

        Args:
            agent_id: Unique identifier for the agent
            domain: Domain specialization
            version: Agent version
            capabilities: List of agent capabilities
        """
        self.agent_id = agent_id
        self.domain = domain
        self.version = version
        self.capabilities = capabilities
        self.knowledge_id = f"Elementum-DSA-{domain.upper()}-KNOWLEDGE-V{version}"
        self._initialize()

    @abstractmethod
    def _initialize(self):
        """Initialize agent-specific resources."""
        pass

    @abstractmethod
    def process_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a user query.

        Args:
            query: The user query
            context: Optional context information

        Returns:
            Response dictionary with results
        """
        pass

    @abstractmethod
    def validate_response(self, response: Dict[str, Any]) -> bool:
        """Validate agent response.

        Args:
            response: The response to validate

        Returns:
            True if valid, False otherwise
        """
        pass

    def __str__(self) -> str:
        """String representation of the agent."""
        return f"{self.agent_id} (v{self.version}) - {self.domain}"
