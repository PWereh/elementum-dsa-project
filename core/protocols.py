"""Protocol Implementation

This module provides the communication and interaction protocols for agents.
"""

from typing import Dict, Any, List, Callable
from abc import ABC, abstractmethod
from core.agent import Agent


class Protocol(ABC):
    """Base Protocol class for agent interactions."""

    def __init__(self, protocol_id: str, protocol_type: str):
        """Initialize a new Protocol instance.

        Args:
            protocol_id: Unique identifier for the protocol
            protocol_type: Type of protocol (direct, mediated, collaborative, supervised)
        """
        self.protocol_id = protocol_id
        self.protocol_type = protocol_type
        self.handlers = {}

    def register_handler(self, event: str, handler: Callable):
        """Register a handler for an event.

        Args:
            event: Event name
            handler: Handler function
        """
        self.handlers[event] = handler

    def handle_event(self, event: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle an event.

        Args:
            event: Event name
            data: Event data

        Returns:
            Response data
        """
        if event in self.handlers:
            return self.handlers[event](data)
        else:
            return {
                "protocol_id": self.protocol_id,
                "event": event,
                "error": f"No handler registered for event: {event}",
                "status": "error"
            }


class DirectProtocol(Protocol):
    """Direct interaction protocol (Human → DSA)."""

    def __init__(self):
        """Initialize a new DirectProtocol instance."""
        super().__init__("direct_protocol", "direct")
        self.register_handler("query", self._handle_query)

    def _handle_query(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a direct query.

        Args:
            data: Query data

        Returns:
            Response data
        """
        if "agent" not in data or "query" not in data:
            return {
                "protocol_id": self.protocol_id,
                "event": "query",
                "error": "Missing required data: agent, query",
                "status": "error"
            }

        agent = data["agent"]
        query = data["query"]
        context = data.get("context", {})

        try:
            response = agent.process_query(query, context)
            return {
                "protocol_id": self.protocol_id,
                "event": "query",
                "response": response,
                "status": "success"
            }
        except Exception as e:
            return {
                "protocol_id": self.protocol_id,
                "event": "query",
                "error": str(e),
                "status": "error"
            }


class CollaborativeProtocol(Protocol):
    """Collaborative interaction protocol (DSA ↔ DSA)."""

    def __init__(self):
        """Initialize a new CollaborativeProtocol instance."""
        super().__init__("collaborative_protocol", "collaborative")
        self.register_handler("collaborate", self._handle_collaborate)

    def _handle_collaborate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a collaboration request.

        Args:
            data: Collaboration data

        Returns:
            Response data
        """
        if "primary_agent" not in data or "support_agents" not in data or "query" not in data:
            return {
                "protocol_id": self.protocol_id,
                "event": "collaborate",
                "error": "Missing required data: primary_agent, support_agents, query",
                "status": "error"
            }

        primary_agent = data["primary_agent"]
        support_agents = data["support_agents"]
        query = data["query"]
        context = data.get("context", {})

        try:
            # Primary agent processes the query
            primary_response = primary_agent.process_query(query, context)

            # Prepare collaboration context
            collab_context = {
                "primary_response": primary_response,
                "original_query": query,
                "original_context": context
            }

            # Support agents contribute
            support_responses = []
            for agent in support_agents:
                support_response = agent.process_query(query, collab_context)
                support_responses.append(support_response)

            # Primary agent integrates responses
            integrated_response = self._integrate_responses(primary_response, support_responses)

            return {
                "protocol_id": self.protocol_id,
                "event": "collaborate",
                "response": integrated_response,
                "status": "success"
            }
        except Exception as e:
            return {
                "protocol_id": self.protocol_id,
                "event": "collaborate",
                "error": str(e),
                "status": "error"
            }

    def _integrate_responses(self, primary_response: Dict[str, Any], support_responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Integrate responses from multiple agents.

        Args:
            primary_response: Response from primary agent
            support_responses: Responses from support agents

        Returns:
            Integrated response
        """
        # This is a placeholder implementation
        # In a real implementation, this would intelligently integrate the responses
        integrated_response = primary_response.copy()
        integrated_response["support_contributions"] = support_responses
        return integrated_response
