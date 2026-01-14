"""
Application settings and configuration

Centralized configuration management using environment variables and defaults.
Extensible through environment-specific configs.
"""

from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class Settings:
    """
    Application settings
    
    To extend:
    1. Add new fields with defaults
    2. Load from environment variables in __post_init__
    3. Consider using python-dotenv for .env file support
    """
    
    # App metadata
    app_name: str = "Tool Hub"
    app_description: str = "A centralized hub for all development tools and guides"
    app_version: str = "1.0.0"
    
    # UI settings
    page_title: str = "Development Tools Hub"
    page_icon: str = "🛠️"
    layout: str = "wide"
    theme_primary_color: str = "#0066cc"
    
    # Feature flags - easily enable/disable features
    enable_search: bool = True
    enable_favorites: bool = True
    enable_analytics: bool = False
    
    # Data source
    tools_config_path: str = "config/tools.yaml"
    
    # Optional: API configuration for future backend integration
    api_base_url: Optional[str] = None
    api_timeout: int = 30
    
    def __post_init__(self):
        """Load settings from environment variables if available"""
        self.app_name = os.getenv("APP_NAME", self.app_name)
        self.app_description = os.getenv("APP_DESCRIPTION", self.app_description)
        self.page_title = os.getenv("PAGE_TITLE", self.page_title)
        self.tools_config_path = os.getenv("TOOLS_CONFIG_PATH", self.tools_config_path)
        
        # Feature flags from environment
        self.enable_search = os.getenv("ENABLE_SEARCH", "true").lower() == "true"
        self.enable_favorites = os.getenv("ENABLE_FAVORITES", "true").lower() == "true"
        self.enable_analytics = os.getenv("ENABLE_ANALYTICS", "false").lower() == "true"
        
        # API config
        self.api_base_url = os.getenv("API_BASE_URL", self.api_base_url)
    
    @classmethod
    def load(cls) -> 'Settings':
        """Factory method to load settings"""
        return cls()


# Global settings instance
settings = Settings.load()
