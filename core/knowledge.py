"""Knowledge Base Implementation

This module provides the structure and interfaces for agent knowledge bases.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from core.errors import KnowledgeException, ValidationException

# Try to import jsonschema for validation
try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

logger = logging.getLogger(__name__)

class KnowledgeBase(ABC):
    """Base knowledge base class for domain-specific agents."""

    def __init__(self, knowledge_id: str, domain: str, version: float, validate: bool = True):
        """Initialize a new KnowledgeBase instance.

        Args:
            knowledge_id: Unique identifier for the knowledge base
            domain: Domain specialization
            version: Knowledge base version
            validate: Whether to validate the knowledge base
        """
        self.knowledge_id = knowledge_id
        self.domain = domain
        self.version = version
        self.core_knowledge = self._load_core_knowledge()
        self.rules = self._load_rules()
        self.best_practices = self._load_best_practices()
        self.validation = self._load_validation()
        self.integration = self._load_integration()
        
        # Validate the knowledge base
        if validate:
            self.validate()

    @abstractmethod
    def _load_core_knowledge(self) -> Dict[str, Any]:
        """Load core domain knowledge.

        Returns:
            Dictionary of core knowledge
        """
        pass

    @abstractmethod
    def _load_rules(self) -> Dict[str, Any]:
        """Load domain-specific rules.

        Returns:
            Dictionary of rules
        """
        pass

    @abstractmethod
    def _load_best_practices(self) -> Dict[str, Any]:
        """Load best practices.

        Returns:
            Dictionary of best practices
        """
        pass

    @abstractmethod
    def _load_validation(self) -> Dict[str, Any]:
        """Load validation rules.

        Returns:
            Dictionary of validation rules
        """
        pass

    @abstractmethod
    def _load_integration(self) -> Dict[str, Any]:
        """Load integration points.

        Returns:
            Dictionary of integration points
        """
        pass

    def get_knowledge(self, category: str = None) -> Dict[str, Any]:
        """Get knowledge from the knowledge base.

        Args:
            category: Optional category filter

        Returns:
            Dictionary of requested knowledge
        """
        if category == "core":
            return self.core_knowledge
        elif category == "rules":
            return self.rules
        elif category == "best_practices":
            return self.best_practices
        elif category == "validation":
            return self.validation
        elif category == "integration":
            return self.integration
        else:
            return {
                "core": self.core_knowledge,
                "rules": self.rules,
                "best_practices": self.best_practices,
                "validation": self.validation,
                "integration": self.integration
            }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the knowledge base to a dictionary.

        Returns:
            Dictionary representation of the knowledge base
        """
        return {
            "knowledge_id": self.knowledge_id,
            "domain": self.domain,
            "version": self.version,
            "core_knowledge": self.core_knowledge,
            "rules": self.rules,
            "best_practices": self.best_practices,
            "validation": self.validation,
            "integration": self.integration
        }
    
    def validate(self) -> bool:
        """Validate the knowledge base against the schema.

        Returns:
            True if validation passes, raises ValidationException otherwise
        """
        if not HAS_JSONSCHEMA:
            logger.warning("jsonschema package not installed. Knowledge base validation skipped.")
            return True
        
        try:
            # Load schema
            schema_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "knowledge", "schemas", "knowledge_schema.json"
            )
            with open(schema_path, "r") as f:
                schema = json.load(f)
            
            # Validate against schema
            knowledge_dict = self.to_dict()
            jsonschema.validate(instance=knowledge_dict, schema=schema)
            logger.info(f"Knowledge base validation passed: {self.knowledge_id}")
            return True
        except FileNotFoundError as e:
            logger.error(f"Schema file not found: {str(e)}")
            raise KnowledgeException(
                f"Schema file not found: {str(e)}",
                domain=self.domain,
                knowledge_id=self.knowledge_id
            )
        except json.JSONDecodeError as e:
            logger.error(f"Invalid schema file: {str(e)}")
            raise KnowledgeException(
                f"Invalid schema file: {str(e)}",
                domain=self.domain,
                knowledge_id=self.knowledge_id
            )
        except jsonschema.exceptions.ValidationError as e:
            logger.error(f"Knowledge base validation failed for {self.knowledge_id}: {str(e)}")
            raise ValidationException(
                f"Knowledge base validation failed: {str(e)}",
                domain=self.domain,
                validation_errors=[str(e)]
            )
        except Exception as e:
            logger.error(f"Unexpected error validating knowledge base {self.knowledge_id}: {str(e)}")
            raise KnowledgeException(
                f"Unexpected error validating knowledge base: {str(e)}",
                domain=self.domain,
                knowledge_id=self.knowledge_id
            )
    
    def save_to_file(self, file_path: str):
        """Save the knowledge base to a JSON file.

        Args:
            file_path: Path to the output file
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            
            # Save to file
            with open(file_path, "w") as f:
                json.dump(self.to_dict(), f, indent=2)
            logger.info(f"Knowledge base saved to {file_path}")
        except Exception as e:
            logger.error(f"Error saving knowledge base to {file_path}: {str(e)}")
            raise KnowledgeException(
                f"Error saving knowledge base to file: {str(e)}",
                domain=self.domain,
                knowledge_id=self.knowledge_id
            )
    
    @classmethod
    def load_from_file(cls, file_path: str, domain: str, version: float) -> 'KnowledgeBase':
        """Load a knowledge base from a JSON file.
        
        This is a template method that should be implemented by subclasses.

        Args:
            file_path: Path to the input file
            domain: Domain specialization
            version: Knowledge base version

        Returns:
            Loaded knowledge base instance
        """
        raise NotImplementedError("Load from file not implemented for base KnowledgeBase class")
