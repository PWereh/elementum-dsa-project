"""Master Control Agent Implementation

This module provides the Master Control Agent (MCA) implementation for managing domain-specific agents.
"""

from typing import Dict, Any, List, Optional
import logging
from core.agent import Agent
from core.governance import GovernanceEngine
from core.monitoring import MonitoringSystem
from core.protocols import DirectProtocol, CollaborativeProtocol
from core.errors import AgentException, format_error_response

logger = logging.getLogger(__name__)

class MasterControlAgent:
    """Master Control Agent for managing domain-specific agents."""

    def __init__(self):
        """Initialize a new MasterControlAgent instance."""
        self.agents = {}
        self.governance = GovernanceEngine()
        self.monitoring = MonitoringSystem()
        self.direct_protocol = DirectProtocol()
        self.collaborative_protocol = CollaborativeProtocol()

    def register_agent(self, agent: Agent):
        """Register a domain-specific agent.

        Args:
            agent: The agent to register
        """
        self.agents[agent.agent_id] = agent
        logger.info(f"Registered agent: {agent}")

    def unregister_agent(self, agent_id: str):
        """Unregister a domain-specific agent.

        Args:
            agent_id: The agent ID to unregister
        """
        if agent_id in self.agents:
            agent = self.agents.pop(agent_id)
            logger.info(f"Unregistered agent: {agent}")
        else:
            logger.warning(f"Agent not found: {agent_id}")

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get a registered agent by ID.

        Args:
            agent_id: The agent ID

        Returns:
            The agent or None if not found
        """
        return self.agents.get(agent_id)

    def get_agents_by_domain(self, domain: str) -> List[Agent]:
        """Get all registered agents for a domain.

        Args:
            domain: The domain to filter by

        Returns:
            List of matching agents
        """
        return [agent for agent in self.agents.values() if agent.domain == domain]

    def determine_agent(self, query: str, domain: str = None) -> Optional[str]:
        """Determine the appropriate agent for a query.

        Args:
            query: The query to process
            domain: Optional domain to filter by

        Returns:
            Agent ID or None if no appropriate agent found
        """
        try:
            # If domain is specified, use the first agent for that domain
            if domain:
                domain_agents = self.get_agents_by_domain(domain)
                if domain_agents:
                    return domain_agents[0].agent_id
                logger.warning(f"No agents found for domain: {domain}")
                return None

            # Simple keyword-based agent selection
            # In a real implementation, this would use NLP or more sophisticated matching
            keywords = {
                "presentation": "presentation_development",
                "slide": "presentation_development",
                "powerpoint": "presentation_development",
                "data": "data_analysis",
                "analysis": "data_analysis",
                "statistics": "data_analysis",
                "visualization": "data_analysis"
            }

            # Check for keyword matches
            for keyword, match_domain in keywords.items():
                if keyword.lower() in query.lower():
                    domain_agents = self.get_agents_by_domain(match_domain)
                    if domain_agents:
                        return domain_agents[0].agent_id

            # If no matches, use the first available agent
            if self.agents:
                return next(iter(self.agents.keys()))

            logger.warning("No appropriate agent found for query")
            return None
        except Exception as e:
            logger.exception(f"Error determining agent: {str(e)}")
            return None

    def process_query(self, query: str, agent_id: str = None, domain: str = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a query using a registered agent.

        Args:
            query: The query to process
            agent_id: Optional agent ID to use
            domain: Optional domain to filter by
            context: Optional context information

        Returns:
            Response from the agent
        """
        if context is None:
            context = {}

        try:
            # Select agent
            agent = None
            if agent_id:
                agent = self.get_agent(agent_id)
                if not agent:
                    logger.error(f"Agent not found: {agent_id}")
                    return format_error_response(
                        AgentException(f"Agent not found: {agent_id}"),
                        agent_id=agent_id,
                        query=query
                    )
            elif domain:
                domain_agents = self.get_agents_by_domain(domain)
                if domain_agents:
                    # Use the first agent for the domain
                    agent = domain_agents[0]
                else:
                    logger.error(f"No agents found for domain: {domain}")
                    return format_error_response(
                        AgentException(f"No agents found for domain: {domain}"),
                        domain=domain,
                        query=query
                    )
            else:
                # Determine the appropriate agent
                determined_agent_id = self.determine_agent(query)
                if determined_agent_id:
                    agent = self.get_agent(determined_agent_id)
                else:
                    logger.error("Could not determine an appropriate agent and none specified")
                    return format_error_response(
                        AgentException("Could not determine an appropriate agent and none specified"),
                        query=query
                    )

            # Check governance rules
            governance_context = {
                "agent": agent,
                "query": query,
                "context": context
            }
            governance_result = self.governance.enforce(governance_context)

            if governance_result["action"] == "block":
                logger.warning(f"Query blocked by governance rules: {governance_result['message']}")
                return {
                    "error": governance_result["message"],
                    "violations": governance_result["violations"],
                    "status": "blocked"
                }

            # Process query with timing
            self.monitoring.start_timing()
            protocol_data = {
                "agent": agent,
                "query": query,
                "context": context
            }
            protocol_result = self.direct_protocol.handle_event("query", protocol_data)
            response_time = self.monitoring.stop_timing()

            # Record metrics
            if protocol_result["status"] == "success":
                self.monitoring.record_accuracy(protocol_result["response"])

            # Add governance warnings if any
            if governance_result["action"] == "warn":
                if protocol_result["status"] == "success":
                    protocol_result["response"]["warnings"] = governance_result["violations"]
                else:
                    protocol_result["warnings"] = governance_result["violations"]

            # Add performance metrics
            if protocol_result["status"] == "success":
                protocol_result["response"]["performance"] = {
                    "response_time": response_time
                }
            else:
                protocol_result["performance"] = {
                    "response_time": response_time
                }

            return protocol_result
        except Exception as e:
            logger.exception(f"Error processing query: {str(e)}")
            return format_error_response(
                e,
                agent_id=agent_id if agent_id else None,
                domain=domain if domain else None,
                query=query
            )

    def collaborate(self, query: str, primary_agent_id: str, support_agent_ids: List[str], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a query using collaborative agents.

        Args:
            query: The query to process
            primary_agent_id: Primary agent ID
            support_agent_ids: Support agent IDs
            context: Optional context information

        Returns:
            Response from the collaboration
        """
        if context is None:
            context = {}

        try:
            # Get primary agent
            primary_agent = self.get_agent(primary_agent_id)
            if not primary_agent:
                logger.error(f"Primary agent not found: {primary_agent_id}")
                return format_error_response(
                    AgentException(f"Primary agent not found: {primary_agent_id}"),
                    agent_id=primary_agent_id,
                    query=query
                )

            # Get support agents
            support_agents = []
            missing_agents = []
            for agent_id in support_agent_ids:
                agent = self.get_agent(agent_id)
                if agent:
                    support_agents.append(agent)
                else:
                    missing_agents.append(agent_id)

            if missing_agents:
                logger.error(f"Support agents not found: {', '.join(missing_agents)}")
                return format_error_response(
                    AgentException(f"Support agents not found: {', '.join(missing_agents)}"),
                    agent_id=primary_agent_id,
                    query=query
                )

            # Check governance rules for all agents
            governance_results = []
            for agent in [primary_agent] + support_agents:
                governance_context = {
                    "agent": agent,
                    "query": query,
                    "context": context
                }
                governance_result = self.governance.enforce(governance_context)
                governance_results.append({
                    "agent_id": agent.agent_id,
                    "result": governance_result
                })

            # Check for blocked agents
            blocked_agents = [result for result in governance_results if result["result"]["action"] == "block"]
            if blocked_agents:
                logger.warning(f"Collaboration blocked due to governance violations: {blocked_agents}")
                return {
                    "error": "Collaboration blocked due to governance violations",
                    "blocked_agents": blocked_agents,
                    "status": "blocked"
                }

            # Process collaborative query with timing
            self.monitoring.start_timing()
            protocol_data = {
                "primary_agent": primary_agent,
                "support_agents": support_agents,
                "query": query,
                "context": context
            }
            protocol_result = self.collaborative_protocol.handle_event("collaborate", protocol_data)
            response_time = self.monitoring.stop_timing()

            # Record metrics
            if protocol_result["status"] == "success":
                self.monitoring.record_accuracy(protocol_result["response"])

            # Add warning agents if any
            warning_agents = [result for result in governance_results if result["result"]["action"] == "warn"]
            if warning_agents:
                if protocol_result["status"] == "success":
                    protocol_result["response"]["warnings"] = warning_agents
                else:
                    protocol_result["warnings"] = warning_agents

            # Add performance metrics
            if protocol_result["status"] == "success":
                protocol_result["response"]["performance"] = {
                    "response_time": response_time
                }
            else:
                protocol_result["performance"] = {
                    "response_time": response_time
                }

            return protocol_result
        except Exception as e:
            logger.exception(f"Error in collaboration: {str(e)}")
            return format_error_response(
                e,
                agent_id=primary_agent_id,
                query=query
            )

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for all agents.

        Returns:
            Dictionary of performance metrics
        """
        return self.monitoring.get_metrics_summary()
