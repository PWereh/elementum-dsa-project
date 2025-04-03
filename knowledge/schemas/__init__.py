"""JSON schemas for validating agent and knowledge base definitions."""

import json
import os
from typing import Dict, Any


def load_schema(schema_name: str) -> Dict[str, Any]:
    """Load a JSON schema from the schemas directory.

    Args:
        schema_name: Name of the schema file (without .json extension)

    Returns:
        The loaded schema as a dictionary
    """
    schema_path = os.path.join(os.path.dirname(__file__), f"{schema_name}.json")
    with open(schema_path, "r") as f:
        return json.load(f)


def get_agent_schema() -> Dict[str, Any]:
    """Get the agent schema.

    Returns:
        The agent schema as a dictionary
    """
    return load_schema("agent_schema")


def get_knowledge_schema() -> Dict[str, Any]:
    """Get the knowledge base schema.

    Returns:
        The knowledge base schema as a dictionary
    """
    return load_schema("knowledge_schema")


__all__ = [
    'load_schema',
    'get_agent_schema',
    'get_knowledge_schema',
]