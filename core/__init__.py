"""Core components for the Elementum DSA framework."""

from core.agent import Agent
from core.knowledge import KnowledgeBase
from core.protocols import Protocol, DirectProtocol, CollaborativeProtocol
from core.governance import GovernanceEngine, GovernanceRule
from core.monitoring import MonitoringSystem, PerformanceMetric
from core.mca import MasterControlAgent
from core.errors import (
    DomainException, ValidationException, 
    KnowledgeException, AgentException, 
    ProtocolException, format_error_response
)

__all__ = [
    'Agent',
    'KnowledgeBase',
    'Protocol',
    'DirectProtocol',
    'CollaborativeProtocol',
    'GovernanceEngine',
    'GovernanceRule',
    'MonitoringSystem',
    'PerformanceMetric',
    'MasterControlAgent',
    'DomainException',
    'ValidationException',
    'KnowledgeException',
    'AgentException',
    'ProtocolException',
    'format_error_response',
]