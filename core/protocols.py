"""Protocol Implementation

This module provides the communication and interaction protocols for agents.
"""

from typing import Dict, Any, List, Callable, Optional
from abc import ABC, abstractmethod
import logging
from core.agent import Agent

logger = logging.getLogger("elementum_dsa.protocols")

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
            logger.debug(f"Handling event '{event}' with protocol '{self.protocol_id}'")
            return self.handlers[event](data)
        else:
            logger.warning(f"No handler registered for event '{event}' in protocol '{self.protocol_id}'")
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
            logger.error("Missing required data in direct protocol: agent, query")
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
            logger.info(f"Processing query with agent '{agent.agent_id}': {query}")
            response = agent.process_query(query, context)
            
            if not agent.validate_response(response):
                logger.warning(f"Agent '{agent.agent_id}' returned an invalid response")
                return {
                    "protocol_id": self.protocol_id,
                    "event": "query",
                    "error": "Agent returned an invalid response",
                    "status": "error"
                }
            
            return {
                "protocol_id": self.protocol_id,
                "event": "query",
                "response": response,
                "status": "success"
            }
        except Exception as e:
            logger.exception(f"Error processing query with agent '{agent.agent_id}': {str(e)}")
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
            logger.error("Missing required data in collaborative protocol: primary_agent, support_agents, query")
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
            logger.info(f"Primary agent '{primary_agent.agent_id}' processing query: {query}")
            primary_response = primary_agent.process_query(query, context)
            
            if not primary_agent.validate_response(primary_response):
                logger.warning(f"Primary agent '{primary_agent.agent_id}' returned an invalid response")
                return {
                    "protocol_id": self.protocol_id,
                    "event": "collaborate",
                    "error": "Primary agent returned an invalid response",
                    "status": "error"
                }

            # Extract relevant information from primary response
            primary_info = self._extract_response_info(primary_response)
            
            # Prepare collaboration context
            collab_context = {
                "primary_response": primary_info,
                "original_query": query,
                "original_context": context,
                "collaboration_type": "enhancement"
            }

            # Support agents contribute
            support_responses = []
            for agent in support_agents:
                logger.info(f"Support agent '{agent.agent_id}' processing collaboration")
                
                # Create agent-specific collaboration query
                collab_query = self._generate_collaboration_query(query, primary_info, agent)
                
                # Process the collaboration query
                support_response = agent.process_query(collab_query, collab_context)
                
                if not agent.validate_response(support_response):
                    logger.warning(f"Support agent '{agent.agent_id}' returned an invalid response")
                    continue
                
                support_responses.append(support_response)

            # Primary agent integrates responses
            logger.info(f"Integrating {len(support_responses)} support responses")
            integrated_response = self._integrate_responses(primary_response, support_responses)

            return {
                "protocol_id": self.protocol_id,
                "event": "collaborate",
                "response": integrated_response,
                "status": "success"
            }
        except Exception as e:
            logger.exception(f"Error in collaboration: {str(e)}")
            return {
                "protocol_id": self.protocol_id,
                "event": "collaborate",
                "error": str(e),
                "status": "error"
            }

    def _extract_response_info(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant information from a response for collaboration.

        Args:
            response: The response to extract information from

        Returns:
            Extracted information
        """
        # Extract only the necessary information for collaboration
        extracted = {
            "agent_id": response.get("agent_id"),
            "domain": response.get("domain"),
            "response": response.get("response"),
            "status": response.get("status")
        }
        
        # Extract additional fields if available
        for key in ["data", "metadata", "recommendations"]:
            if key in response:
                extracted[key] = response[key]
                
        return extracted
    
    def _generate_collaboration_query(self, original_query: str, primary_info: Dict[str, Any], support_agent: Agent) -> str:
        """Generate a collaboration query for a support agent.

        Args:
            original_query: The original query
            primary_info: Information from the primary agent's response
            support_agent: The support agent

        Returns:
            Collaboration query
        """
        # Determine what kind of support is needed based on agent capabilities
        if "data_analysis" in support_agent.domain:
            return f"Analyze the following content and provide insights: {primary_info.get('response', '')}"
        elif "presentation_development" in support_agent.domain:
            return f"Create a presentation structure for the following content: {primary_info.get('response', '')}"
        else:
            # Generic collaboration query
            return f"Enhance the following with your expertise: {primary_info.get('response', '')}"

    def _integrate_responses(self, primary_response: Dict[str, Any], support_responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Integrate responses from multiple agents.

        Args:
            primary_response: Response from primary agent
            support_responses: Responses from support agents

        Returns:
            Integrated response
        """
        integrated_response = primary_response.copy()
        
        # Create a more structured integration of support contributions
        contributions = []
        for response in support_responses:
            contribution = {
                "agent_id": response.get("agent_id"),
                "domain": response.get("domain"),
                "content": response.get("response")
            }
            contributions.append(contribution)
        
        # Add the contributions to the integrated response
        integrated_response["support_contributions"] = contributions
        
        # Combine key insights if available
        all_insights = []
        for response in support_responses:
            if "data" in response and "insights" in response["data"]:
                all_insights.extend(response["data"]["insights"])
        
        if all_insights:
            if "data" not in integrated_response:
                integrated_response["data"] = {}
            integrated_response["data"]["combined_insights"] = all_insights
        
        # Add integration metadata
        integrated_response["integration_info"] = {
            "primary_agent": primary_response.get("agent_id"),
            "support_agents": [r.get("agent_id") for r in support_responses],
            "integration_type": "enhancement"
        }
        
        return integrated_response


class MediatedProtocol(Protocol):
    """Mediated interaction protocol (Human → MCA → DSA)."""

    def __init__(self, master_control_agent):
        """Initialize a new MediatedProtocol instance.

        Args:
            master_control_agent: The Master Control Agent
        """
        super().__init__("mediated_protocol", "mediated")
        self.mca = master_control_agent
        self.register_handler("mediated_query", self._handle_mediated_query)

    def _handle_mediated_query(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a mediated query.

        Args:
            data: Query data

        Returns:
            Response data
        """
        if "query" not in data:
            logger.error("Missing required data in mediated protocol: query")
            return {
                "protocol_id": self.protocol_id,
                "event": "mediated_query",
                "error": "Missing required data: query",
                "status": "error"
            }

        query = data["query"]
        domain = data.get("domain")
        context = data.get("context", {})

        try:
            # Let the MCA determine the appropriate agent
            logger.info(f"MCA processing mediated query: {query}")
            agent_id = self.mca.determine_agent(query, domain)
            
            if not agent_id:
                logger.warning(f"MCA could not determine an appropriate agent for the query: {query}")
                return {
                    "protocol_id": self.protocol_id,
                    "event": "mediated_query",
                    "error": "Could not determine an appropriate agent for the query",
                    "status": "error"
                }
            
            # Process the query with the determined agent
            agent = self.mca.get_agent(agent_id)
            response = agent.process_query(query, context)
            
            return {
                "protocol_id": self.protocol_id,
                "event": "mediated_query",
                "response": response,
                "status": "success"
            }
        except Exception as e:
            logger.exception(f"Error in mediated query: {str(e)}")
            return {
                "protocol_id": self.protocol_id,
                "event": "mediated_query",
                "error": str(e),
                "status": "error"
            }
