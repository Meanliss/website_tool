"""
Tool Service - Business logic layer

Handles all tool-related operations: filtering, searching, categorization.
Separates business logic from UI and data layers.
"""

from typing import List, Dict, Optional
from collections import defaultdict

from models.tool import Tool, ToolCategory
from app_config.tools_config import get_tools_config


class ToolService:
    """
    Service layer for tool operations
    
    Follows Service Pattern for clean separation of concerns.
    Extensible through:
    - Adding new filtering methods
    - Implementing caching strategies
    - Adding analytics/logging
    - Integrating with external APIs
    """
    
    def __init__(self, config_path: str = "config/tools.yaml"):
        """
        Initialize service with tools from configuration
        
        Args:
            config_path: Path to tools configuration file
        """
        self.config_path = config_path
        self._tools: List[Tool] = []
        self._tools_by_id: Dict[str, Tool] = {}
        self._tools_by_category: Dict[ToolCategory, List[Tool]] = defaultdict(list)
        self.load_tools()
    
    def load_tools(self):
        """
        Load tools from configuration
        
        Extensible: Add caching, validation, or API fetching here
        """
        self._tools = get_tools_config(self.config_path)
        
        # Build indexes for fast lookups
        self._tools_by_id = {tool.id: tool for tool in self._tools}
        
        self._tools_by_category = defaultdict(list)
        for tool in self._tools:
            self._tools_by_category[tool.category].append(tool)
    
    def reload_tools(self):
        """Reload tools from configuration (useful for dynamic updates)"""
        self.load_tools()
    
    def get_all_tools(self) -> List[Tool]:
        """Get all tools"""
        return self._tools.copy()
    
    def get_tool_by_id(self, tool_id: str) -> Optional[Tool]:
        """
        Get a specific tool by ID
        
        Args:
            tool_id: Unique tool identifier
        
        Returns:
            Tool object or None if not found
        """
        return self._tools_by_id.get(tool_id)
    
    def get_tools_by_category(self, category: ToolCategory) -> List[Tool]:
        """
        Get all tools in a specific category
        
        Args:
            category: Tool category
        
        Returns:
            List of tools in that category
        """
        return self._tools_by_category.get(category, []).copy()
    
    def get_categories_with_tools(self) -> Dict[ToolCategory, List[Tool]]:
        """
        Get all categories that have tools
        
        Returns:
            Dictionary mapping categories to their tools
        """
        return {
            category: tools.copy()
            for category, tools in self._tools_by_category.items()
            if tools
        }
    
    def search_tools(self, query: str) -> List[Tool]:
        """
        Search tools by name, description, or tags
        
        Args:
            query: Search query string
        
        Returns:
            List of matching tools
        
        Extensible:
        - Add fuzzy matching
        - Add relevance scoring
        - Add search analytics
        """
        if not query:
            return self.get_all_tools()
        
        return [tool for tool in self._tools if tool.matches_search(query)]
    
    def filter_tools(
        self,
        category: Optional[ToolCategory] = None,
        tags: Optional[List[str]] = None,
        is_external: Optional[bool] = None
    ) -> List[Tool]:
        """
        Filter tools by multiple criteria
        
        Args:
            category: Filter by category
            tags: Filter by tags (tool must have at least one)
            is_external: Filter by external/internal status
        
        Returns:
            List of filtered tools
        
        Extensible: Add more filter criteria as needed
        """
        filtered = self._tools
        
        if category is not None:
            filtered = [t for t in filtered if t.category == category]
        
        if tags is not None and tags:
            filtered = [
                t for t in filtered
                if any(tag.lower() in [tt.lower() for tt in t.tags] for tag in tags)
            ]
        
        if is_external is not None:
            filtered = [t for t in filtered if t.is_external == is_external]
        
        return filtered
    
    def get_tools_count(self) -> int:
        """Get total number of tools"""
        return len(self._tools)
    
    def get_categories_count(self) -> int:
        """Get number of categories with tools"""
        return len(self._tools_by_category)
    
    def get_statistics(self) -> Dict[str, any]:
        """
        Get system statistics
        
        Returns:
            Dictionary with various statistics
        
        Extensible: Add more metrics as needed
        """
        return {
            'total_tools': self.get_tools_count(),
            'total_categories': self.get_categories_count(),
            'tools_by_category': {
                cat.display_name: len(tools)
                for cat, tools in self._tools_by_category.items()
            },
            'external_tools': len([t for t in self._tools if t.is_external]),
            'internal_tools': len([t for t in self._tools if not t.is_external]),
        }
    
    def get_popular_tags(self, limit: int = 10) -> List[tuple]:
        """
        Get most popular tags
        
        Args:
            limit: Maximum number of tags to return
        
        Returns:
            List of (tag, count) tuples
        
        Useful for tag cloud or filtering UI
        """
        tag_counts = defaultdict(int)
        for tool in self._tools:
            for tag in tool.tags:
                tag_counts[tag.lower()] += 1
        
        return sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
