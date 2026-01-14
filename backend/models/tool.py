"""
Tool data model - Core entity representing a tool in the system

This model uses dataclass for clean, maintainable code and easy serialization.
Extensible through inheritance or composition patterns.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum


class ToolCategory(Enum):
    """
    Tool categories - easily extensible by adding new enum values
    
    To add a new category:
    1. Add new enum value here
    2. Update tools_config.yaml with tools in that category
    3. Optionally customize the icon in category_section.py
    """
    TESTING = "testing"
    DEVELOPMENT = "development"
    AI_ML = "ai_ml"
    DATA = "data"
    DEVOPS = "devops"
    COLLABORATION = "collaboration"
    OTHER = "other"
    
    @property
    def display_name(self) -> str:
        """Human-readable category names"""
        names = {
            self.TESTING: "Testing & QA",
            self.DEVELOPMENT: "Development",
            self.AI_ML: "AI & Machine Learning",
            self.DATA: "Data Tools",
            self.DEVOPS: "DevOps & Infrastructure",
            self.COLLABORATION: "Collaboration",
            self.OTHER: "Other Tools"
        }
        return names.get(self, self.value.replace("_", " ").title())


@dataclass
class Tool:
    """
    Core Tool model
    
    Attributes:
        id: Unique identifier for the tool
        name: Display name of the tool
        description: Brief description of what the tool does
        category: Category this tool belongs to
        url: Optional link to the tool (external URL or internal route)
        icon: Optional emoji or icon identifier
        tags: List of searchable tags
        guide_content: Optional markdown content for usage guide
        is_external: Whether the URL points to an external resource
    
    Extensibility:
    - Add new fields as needed (version, author, rating, etc.)
    - Create subclasses for specialized tool types
    - Use composition for complex features (e.g., Tool has-a Configuration)
    """
    id: str
    name: str
    description: str
    category: ToolCategory
    url: Optional[str] = None
    icon: Optional[str] = "🔧"
    tags: List[str] = field(default_factory=list)
    guide_content: Optional[str] = None
    is_external: bool = True
    
    def __post_init__(self):
        """Validate data after initialization"""
        if not self.id:
            raise ValueError("Tool ID cannot be empty")
        if not self.name:
            raise ValueError("Tool name cannot be empty")
        
        # Convert category string to enum if needed
        if isinstance(self.category, str):
            self.category = ToolCategory(self.category.lower())
    
    def matches_search(self, query: str) -> bool:
        """
        Check if tool matches search query
        
        Extensible: Override this method for custom search logic
        """
        query_lower = query.lower()
        return (
            query_lower in self.name.lower() or
            query_lower in self.description.lower() or
            any(query_lower in tag.lower() for tag in self.tags)
        )
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category.value,
            'url': self.url,
            'icon': self.icon,
            'tags': self.tags,
            'guide_content': self.guide_content,
            'is_external': self.is_external
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Tool':
        """Create Tool instance from dictionary"""
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            category=ToolCategory(data['category']),
            url=data.get('url'),
            icon=data.get('icon', '🔧'),
            tags=data.get('tags', []),
            guide_content=data.get('guide_content'),
            is_external=data.get('is_external', True)
        )
