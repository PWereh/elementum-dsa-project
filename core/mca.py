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

logger = logging.getLogger("elementum_dsa.mca")

class MasterControlAgent:
    """Master Control Agent for managing domain-specific agents."""

    def __init__(self):
        """Initialize a new MasterControlAgent instance."""
        self.agents = {}
        self.domain_agents = {}
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
        
        # Also track by domain for easy lookup
        if agent.domain not in self.domain_agents:
            self.domain_agents[agent.domain] = []
        self.domain_agents[agent.domain].append(agent.agent_id)
        
        logger.info(f"Registered agent: {agent}")

    def unregister_agent(self, agent_id: str):
        """Unregister a domain-specific agent.

        Args:
            agent_id: The agent ID to unregister
        """
        if agent_id in self.agents:
            agent = self.agents.pop(agent_id)
            
            # Also remove from domain lookup
            if agent.domain in self.domain_agents:
                if agent_id in self.domain_agents[agent.domain]:
                    self.domain_agents[agent.domain].remove(agent_id)
                    # Clean up empty domain entries
                    if not self.domain_agents[agent.domain]:
                        del self.domain_agents[agent.domain]
            
            logger.info(f"Unregistered agent: {agent}")
        else:
            logger.warning(f"Agent not found for unregistration: {agent_id}")

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
        agents = []
        if domain in self.domain_agents:
            for agent_id in self.domain_agents[domain]:
                agent = self.get_agent(agent_id)
                if agent:
                    agents.append(agent)
        return agents
    
    def determine_agent(self, query: str, domain: str = None) -> Optional[str]:
        """Determine the appropriate agent for a query.

        Args:
            query: The query to process
            domain: Optional domain to filter by

        Returns:
            ID of the appropriate agent or None if not found
        """
        # If domain is specified, use it to find an agent
        if domain:
            domain_agents = self.get_agents_by_domain(domain)
            if domain_agents:
                # Return the first agent for the domain
                return domain_agents[0].agent_id
        
        # If no domain is specified or no agents found for domain,
        # try to determine the appropriate agent based on the query
        # This is a simple implementation - in a real system, this would use
        # more sophisticated NLP techniques to analyze the query
        
        # Look for domain-specific keywords in the query
        for domain_name, agent_ids in self.domain_agents.items():
            if domain_name.lower() in query.lower():
                if agent_ids:
                    return agent_ids[0]
        
        # If no match found, return None
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
                    error_msg = f"Agent not found: {agent_id}"
                    logger.error(error_msg)
                    return format_error_response(
                        AgentException(error_msg, agent_id=agent_id),
                        agent_id=agent_id,
                        query=query
                    )
            elif domain:
                domain_agents = self.get_agents_by_domain(domain)
                if domain_agents:
                    # Use the first agent for the domain
                    agent = domain_agents[0]
                else:
                    error_msg = f"No agents found for domain: {domain}"
                    logger.error(error_msg)
                    return format_error_response(
                        AgentException(error_msg, domain=domain),
                        domain=domain,
                        query=query
                    )
            else:
                # Try to determine the appropriate agent
                determined_agent_id = self.determine_agent(query)
                if determined_agent_id:
                    agent = self.get_agent(determined_agent_id)
                else:
                    error_msg = "Could not determine an appropriate agent. Please specify agent_id or domain."
                    logger.error(error_msg)
                    return format_error_response(
                        AgentException(error_msg),
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
                error_msg = governance_result["message"]
                logger.warning(f"Query blocked by governance: {error_msg}")
                return {
                    "error": error_msg,
                    "violations": governance_result["violations"],
                    "status": "blocked",
                    "agent_id": agent.agent_id,
                    "domain": agent.domain,
                    "query": query
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
                agent_id=agent_id,
                domain=domain,
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
                error_msg = f"Primary agent not found: {primary_agent_id}"
                logger.error(error_msg)
                return format_error_response(
                    AgentException(error_msg, agent_id=primary_agent_id),
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
                error_msg = f"Support agents not found: {', '.join(missing_agents)}"
                logger.error(error_msg)
                return format_error_response(
                    AgentException(error_msg),
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
                error_msg = "Collaboration blocked due to governance violations"
                logger.warning(f"{error_msg}: {blocked_agents}")
                return {
                    "error": error_msg,
                    "blocked_agents": blocked_agents,
                    "status": "blocked",
                    "query": query
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
