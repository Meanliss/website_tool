"""
Tools configuration loader

Loads tool definitions from YAML configuration file.
Supports multiple data sources (YAML, JSON, Database, API) through strategy pattern.
"""

import yaml
import json
from pathlib import Path
from typing import List, Dict, Any
from abc import ABC, abstractmethod

from models.tool import Tool, ToolCategory


class ConfigLoader(ABC):
    """
    Abstract base class for configuration loaders
    
    Extensibility: Implement this interface to load from different sources
    (Database, API, JSON, etc.)
    """
    
    @abstractmethod
    def load_tools(self) -> List[Dict[str, Any]]:
        """Load and return raw tool data"""
        pass


class YAMLConfigLoader(ConfigLoader):
    """Load tools from YAML file"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
    
    def load_tools(self) -> List[Dict[str, Any]]:
        """Load tools from YAML configuration"""
        if not self.file_path.exists():
            return self._get_default_tools()
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return data.get('tools', [])
        except Exception as e:
            print(f"Error loading tools config: {e}")
            return self._get_default_tools()
    
    def _get_default_tools(self) -> List[Dict[str, Any]]:
        """Return default tools if config file doesn't exist"""
        return [
            {
                'id': 'example-tool',
                'name': 'Example Tool',
                'description': 'This is an example tool. Add your tools in config/tools.yaml',
                'category': 'other',
                'icon': '📝',
                'url': 'https://example.com',
                'tags': ['example', 'demo'],
                'is_external': True
            }
        ]


class JSONConfigLoader(ConfigLoader):
    """
    Load tools from JSON file
    
    Example of extensibility - add different loader implementations
    """
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
    
    def load_tools(self) -> List[Dict[str, Any]]:
        """Load tools from JSON configuration"""
        if not self.file_path.exists():
            return []
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('tools', [])
        except Exception as e:
            print(f"Error loading JSON config: {e}")
            return []


def get_tools_config(config_path: str = "config/tools.yaml") -> List[Tool]:
    """
    Load and parse tools configuration
    
    Args:
        config_path: Path to configuration file
    
    Returns:
        List of Tool objects
    
    Extensibility:
    - Add support for different file formats by checking extension
    - Add caching layer for performance
    - Add validation layer
    """
    
    # Determine loader based on file extension
    path = Path(config_path)
    
    if path.suffix in ['.yaml', '.yml']:
        loader = YAMLConfigLoader(config_path)
    elif path.suffix == '.json':
        loader = JSONConfigLoader(config_path)
    else:
        # Default to YAML
        loader = YAMLConfigLoader(config_path)
    
    # Load raw data
    tools_data = loader.load_tools()
    
    # Convert to Tool objects
    tools = []
    for tool_dict in tools_data:
        try:
            tool = Tool.from_dict(tool_dict)
            tools.append(tool)
        except Exception as e:
            print(f"Error parsing tool {tool_dict.get('id', 'unknown')}: {e}")
    
    return tools


def create_sample_config(output_path: str = "config/tools.yaml"):
    """
    Create a sample configuration file
    
    Useful for first-time setup or documentation
    """
    sample_tools = {
        'tools': [
            {
                'id': 'system-test-sw',
                'name': 'System Test SW Testing',
                'description': 'Software testing tools and documentation for system testing',
                'category': 'testing',
                'icon': '🧪',
                'url': 'https://cccn.apac.bosch.com/OSS-CN_DT_AI_HomePage/#/system-test-sw-testing',
                'tags': ['testing', 'qa', 'system-test'],
                'is_external': True,
                'guide_content': '# System Test SW Testing\n\nDetailed guide on how to use this tool...'
            },
            {
                'id': 'python-guide',
                'name': 'Python Development Guide',
                'description': 'Internal guide for Python best practices',
                'category': 'development',
                'icon': '🐍',
                'tags': ['python', 'development', 'guide'],
                'is_external': False,
                'guide_content': '# Python Development\n\n## Setup\n...'
            },
            {
                'id': 'docker-hub',
                'name': 'Docker Hub',
                'description': 'Container registry and Docker resources',
                'category': 'devops',
                'icon': '🐳',
                'url': 'https://hub.docker.com',
                'tags': ['docker', 'containers', 'devops'],
                'is_external': True
            }
        ]
    }
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(sample_tools, f, default_flow_style=False, allow_unicode=True)
    
    print(f"Sample configuration created at {output_path}")
