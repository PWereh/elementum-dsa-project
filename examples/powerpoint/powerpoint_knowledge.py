"""PowerPoint Knowledge Base Implementation

Example implementation of a PowerPoint domain-specific knowledge base.
"""

from typing import Dict, Any
from knowledge.templates.knowledge_template import DomainKnowledgeBase


class PowerPointKnowledgeBase(DomainKnowledgeBase):
    """PowerPoint presentation knowledge base."""

    def __init__(self, domain: str, version: float):
        """Initialize a new PowerPoint knowledge base.

        Args:
            domain: Domain specialization
            version: Knowledge base version
        """
        super().__init__(domain, version)

    def _load_core_knowledge(self) -> Dict[str, Any]:
        """Load core PowerPoint knowledge.

        Returns:
            Dictionary of core knowledge
        """
        return {
            "concepts": {
                "slide": "Basic unit of a presentation",
                "template": "Reusable design pattern",
                "master": "Slide that defines global settings"
            },
            "terminology": {
                "deck": "Complete presentation file",
                "transition": "Animation between slides",
                "theme": "Consistent design elements"
            },
            "principles": {
                "clarity": "Information should be clear and concise",
                "consistency": "Design elements should be consistent",
                "hierarchy": "Important information should stand out"
            }
        }

    def _load_rules(self) -> Dict[str, Any]:
        """Load PowerPoint-specific rules.

        Returns:
            Dictionary of rules
        """
        return {
            "constraints": {
                "text_amount": "Maximum 6 bullet points per slide",
                "slide_count": "Typical presentation: 1 slide per minute",
                "font_size": "Minimum 18pt for body text, 24pt for headings"
            },
            "requirements": {
                "title_slide": "Must include title, presenter, date",
                "agenda": "Must outline key topics",
                "conclusion": "Must summarize key points"
            },
            "guidelines": {
                "contrast": "Ensure text has sufficient contrast with background",
                "multimedia": "Use relevant images, videos, and diagrams",
                "animations": "Use sparingly and purposefully"
            }
        }

    def _load_best_practices(self) -> Dict[str, Any]:
        """Load PowerPoint best practices.

        Returns:
            Dictionary of best practices
        """
        return {
            "recommended": {
                "simplicity": "Keep designs clean and simple",
                "consistency": "Use consistent fonts and colors",
                "whitespace": "Incorporate ample whitespace"
            },
            "optional": {
                "branding": "Include company logos and colors",
                "handouts": "Provide additional details in notes",
                "timers": "Use timers for paced delivery"
            },
            "discouraged": {
                "text_walls": "Avoid excessive text on slides",
                "complex_animations": "Avoid distracting animations",
                "inconsistent_design": "Avoid mixing multiple design styles"
            }
        }

    def _load_validation(self) -> Dict[str, Any]:
        """Load PowerPoint validation rules.

        Returns:
            Dictionary of validation rules
        """
        return {
            "input": {
                "topic_clarity": "Topic must be clearly defined",
                "audience": "Target audience must be specified",
                "duration": "Presentation duration must be known"
            },
            "process": {
                "structure_check": "Verify logical flow of content",
                "design_consistency": "Verify consistent design elements",
                "media_quality": "Verify image and video quality"
            },
            "output": {
                "readability": "Text must be readable from a distance",
                "navigation": "Presentation flow must be intuitive",
                "timing": "Content must fit within allocated time"
            }
        }

    def _load_integration(self) -> Dict[str, Any]:
        """Load PowerPoint integration points.

        Returns:
            Dictionary of integration points
        """
        return {
            "apis": {
                "ms_graph": "Microsoft Graph API for PowerPoint access",
                "template_service": "Template repository service",
                "image_service": "Image search and optimization"
            },
            "services": {
                "presentation_review": "Automated presentation review",
                "accessibility_check": "Accessibility compliance checking",
                "translation": "Content translation services"
            },
            "data_sources": {
                "design_library": "Pre-approved design elements",
                "content_repository": "Reusable content blocks",
                "media_library": "Approved imagery and videos"
            }
        }
