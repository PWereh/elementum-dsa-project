"""Error handling utilities for the Elementum DSA framework."""

from typing import Dict, Any, List, Optional


class DomainException(Exception):
    """Base exception for domain-specific errors."""

    def __init__(self, message: str, domain: str = None, error_code: str = None):
        """Initialize a new DomainException instance.

        Args:
            message: Error message
            domain: Domain where the error occurred
            error_code: Optional error code
        """
        self.message = message
        self.domain = domain
        self.error_code = error_code
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the exception to a dictionary.

        Returns:
            Dictionary representation of the exception
        """
        return {
            "message": self.message,
            "domain": self.domain,
            "error_code": self.error_code
        }


class ValidationException(DomainException):
    """Exception for validation errors."""

    def __init__(self, message: str, domain: str = None, validation_errors: List[str] = None):
        """Initialize a new ValidationException instance.

        Args:
            message: Error message
            domain: Domain where the error occurred
            validation_errors: List of validation errors
        """
        super().__init__(message, domain, "VALIDATION_ERROR")
        self.validation_errors = validation_errors or []

    def to_dict(self) -> Dict[str, Any]:
        """Convert the exception to a dictionary.

        Returns:
            Dictionary representation of the exception
        """
        result = super().to_dict()
        result["validation_errors"] = self.validation_errors
        return result


class KnowledgeException(DomainException):
    """Exception for knowledge base errors."""

    def __init__(self, message: str, domain: str = None, knowledge_id: str = None):
        """Initialize a new KnowledgeException instance.

        Args:
            message: Error message
            domain: Domain where the error occurred
            knowledge_id: ID of the knowledge base
        """
        super().__init__(message, domain, "KNOWLEDGE_ERROR")
        self.knowledge_id = knowledge_id

    def to_dict(self) -> Dict[str, Any]:
        """Convert the exception to a dictionary.

        Returns:
            Dictionary representation of the exception
        """
        result = super().to_dict()
        result["knowledge_id"] = self.knowledge_id
        return result


class AgentException(DomainException):
    """Exception for agent errors."""

    def __init__(self, message: str, domain: str = None, agent_id: str = None):
        """Initialize a new AgentException instance.

        Args:
            message: Error message
            domain: Domain where the error occurred
            agent_id: ID of the agent
        """
        super().__init__(message, domain, "AGENT_ERROR")
        self.agent_id = agent_id

    def to_dict(self) -> Dict[str, Any]:
        """Convert the exception to a dictionary.

        Returns:
            Dictionary representation of the exception
        """
        result = super().to_dict()
        result["agent_id"] = self.agent_id
        return result


class ProtocolException(DomainException):
    """Exception for protocol errors."""

    def __init__(self, message: str, domain: str = None, protocol_id: str = None):
        """Initialize a new ProtocolException instance.

        Args:
            message: Error message
            domain: Domain where the error occurred
            protocol_id: ID of the protocol
        """
        super().__init__(message, domain, "PROTOCOL_ERROR")
        self.protocol_id = protocol_id

    def to_dict(self) -> Dict[str, Any]:
        """Convert the exception to a dictionary.

        Returns:
            Dictionary representation of the exception
        """
        result = super().to_dict()
        result["protocol_id"] = self.protocol_id
        return result


def format_error_response(error: Exception, agent_id: str = None, domain: str = None, query: str = None) -> Dict[str, Any]:
    """Format an error response.

    Args:
        error: The error that occurred
        agent_id: ID of the agent
        domain: Domain where the error occurred
        query: The query that caused the error

    Returns:
        Formatted error response
    """
    if isinstance(error, DomainException):
        error_data = error.to_dict()
    else:
        error_data = {
            "message": str(error),
            "error_code": "GENERAL_ERROR"
        }

    return {
        "agent_id": agent_id,
        "domain": domain,
        "query": query,
        "error": error_data,
        "status": "error"
    }
