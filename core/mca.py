"""Master Control Agent Implementation

This module provides the Master Control Agent (MCA) implementation for managing domain-specific agents.
"""

from typing import Dict, Any, List, Optional
from core.agent import Agent
from core.governance import GovernanceEngine
from core.monitoring import MonitoringSystem
from core.protocols import DirectProtocol, CollaborativeProtocol


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
        print(f"Registered agent: {agent}")

    def unregister_agent(self, agent_id: str):
        """Unregister a domain-specific agent.

        Args:
            agent_id: The agent ID to unregister
        """
        if agent_id in self.agents:
            agent = self.agents.pop(agent_id)
            print(f"Unregistered agent: {agent}")
        else:
            print(f"Agent not found: {agent_id}")

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

        # Select agent
        agent = None
        if agent_id:
            agent = self.get_agent(agent_id)
            if not agent:
                return {
                    "error": f"Agent not found: {agent_id}",
                    "status": "error"
                }
        elif domain:
            domain_agents = self.get_agents_by_domain(domain)
            if domain_agents:
                # Use the first agent for the domain
                agent = domain_agents[0]
            else:
                return {
                    "error": f"No agents found for domain: {domain}",
                    "status": "error"
                }
        else:
            return {
                "error": "Either agent_id or domain must be specified",
                "status": "error"
            }

        # Check governance rules
        governance_context = {
            "agent": agent,
            "query": query,
            "context": context
        }
        governance_result = self.governance.enforce(governance_context)

        if governance_result["action"] == "block":
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

        # Get primary agent
        primary_agent = self.get_agent(primary_agent_id)
        if not primary_agent:
            return {
                "error": f"Primary agent not found: {primary_agent_id}",
                "status": "error"
            }

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
            return {
                "error": f"Support agents not found: {', '.join(missing_agents)}",
                "status": "error"
            }

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

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for all agents.

        Returns:
            Dictionary of performance metrics
        """
        return self.monitoring.get_metrics_summary()
