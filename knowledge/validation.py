"""Schema validation utilities for the Elementum DSA framework."""

import json
import os
from typing import Dict, Any, Union, List, Optional

# Try to import jsonschema for validation
try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


def load_schema(schema_path: str) -> Dict[str, Any]:
    """Load a JSON schema from a file.

    Args:
        schema_path: Path to the schema file

    Returns:
        The loaded schema as a dictionary
    """
    with open(schema_path, "r") as f:
        return json.load(f)


def get_schema_path(schema_name: str) -> str:
    """Get the path to a schema file.

    Args:
        schema_name: Name of the schema file (without .json extension)

    Returns:
        Path to the schema file
    """
    return os.path.join(os.path.dirname(__file__), "schemas", f"{schema_name}.json")


def validate_against_schema(data: Dict[str, Any], schema_name: str) -> List[str]:
    """Validate data against a JSON schema.

    Args:
        data: Data to validate
        schema_name: Name of the schema to use (without .json extension)

    Returns:
        List of validation errors (empty if validation succeeds)
    """
    if not HAS_JSONSCHEMA:
        return ["jsonschema package is not installed. Install it with 'pip install jsonschema'."]

    schema_path = get_schema_path(schema_name)
    schema = load_schema(schema_path)

    validator = jsonschema.Draft7Validator(schema)
    errors = list(validator.iter_errors(data))
    return [str(error) for error in errors]


def validate_agent(agent_data: Dict[str, Any]) -> List[str]:
    """Validate agent data against the agent schema.

    Args:
        agent_data: Agent data to validate

    Returns:
        List of validation errors (empty if validation succeeds)
    """
    return validate_against_schema(agent_data, "agent_schema")


def validate_knowledge_base(knowledge_data: Dict[str, Any]) -> List[str]:
    """Validate knowledge base data against the knowledge schema.

    Args:
        knowledge_data: Knowledge base data to validate

    Returns:
        List of validation errors (empty if validation succeeds)
    """
    return validate_against_schema(knowledge_data, "knowledge_schema")


def agent_to_dict(agent) -> Dict[str, Any]:
    """Convert an Agent instance to a dictionary for validation.

    Args:
        agent: Agent instance

    Returns:
        Dictionary representation of the agent
    """
    return {
        "agent_id": agent.agent_id,
        "knowledge_id": agent.knowledge_id,
        "domain": agent.domain,
        "version": agent.version,
        "capabilities": agent.capabilities,
        "dependencies": getattr(agent, "dependencies", [])
    }


def knowledge_base_to_dict(knowledge_base) -> Dict[str, Any]:
    """Convert a KnowledgeBase instance to a dictionary for validation.

    Args:
        knowledge_base: KnowledgeBase instance

    Returns:
        Dictionary representation of the knowledge base
    """
    return {
        "knowledge_id": knowledge_base.knowledge_id,
        "domain": knowledge_base.domain,
        "version": knowledge_base.version,
        "core_knowledge": knowledge_base.core_knowledge,
        "rules": knowledge_base.rules,
        "best_practices": knowledge_base.best_practices,
        "validation": knowledge_base.validation,
        "integration": knowledge_base.integration
    }
