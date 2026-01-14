"""
FastAPI Backend for Tool Hub

Main API server providing endpoints for tools data.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from pathlib import Path

# Import local services
from models.tool import Tool, ToolCategory
from services.tool_service import ToolService

# Initialize FastAPI app
app = FastAPI(
    title="Tool Hub API",
    description="API for managing and accessing development tools",
    version="1.0.0"
)

# CORS middleware - allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service
tool_service = ToolService(config_path="config/tools.yaml")

# Pydantic models for API responses
class ToolResponse(BaseModel):
    id: str
    name: str
    description: str
    category: str
    url: Optional[str] = None
    icon: Optional[str] = "🔧"
    tags: List[str] = []
    guide_content: Optional[str] = None
    is_external: bool = True

class StatsResponse(BaseModel):
    total_tools: int
    total_categories: int
    tools_by_category: dict
    external_tools: int
    internal_tools: int

class CategoryInfo(BaseModel):
    value: str
    display_name: str

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Tool Hub API",
        "version": "1.0.0",
        "endpoints": {
            "tools": "/api/tools",
            "categories": "/api/categories",
            "stats": "/api/stats"
        }
    }

@app.get("/api/tools", response_model=List[ToolResponse])
async def get_tools(
    category: Optional[str] = None,
    search: Optional[str] = None,
    tags: Optional[str] = None,
    is_external: Optional[bool] = None
):
    """
    Get all tools with optional filters
    
    Query parameters:
    - category: Filter by category
    - search: Search in name, description, tags
    - tags: Comma-separated tags to filter by
    - is_external: Filter by external/internal tools
    """
    tools = tool_service.get_all_tools()
    
    # Apply filters
    if search:
        tools = [t for t in tools if t.matches_search(search)]
    
    if category:
        try:
            cat = ToolCategory(category.lower())
            tools = [t for t in tools if t.category == cat]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    
    if tags:
        tag_list = [t.strip().lower() for t in tags.split(',')]
        tools = [
            t for t in tools
            if any(tag in [tt.lower() for tt in t.tags] for tag in tag_list)
        ]
    
    if is_external is not None:
        tools = [t for t in tools if t.is_external == is_external]
    
    # Convert to response format
    return [
        ToolResponse(
            id=t.id,
            name=t.name,
            description=t.description,
            category=t.category.value,
            url=t.url,
            icon=t.icon,
            tags=t.tags,
            guide_content=t.guide_content,
            is_external=t.is_external
        )
        for t in tools
    ]

@app.get("/api/tools/{tool_id}", response_model=ToolResponse)
async def get_tool(tool_id: str):
    """Get a specific tool by ID"""
    tool = tool_service.get_tool_by_id(tool_id)
    
    if not tool:
        raise HTTPException(status_code=404, detail=f"Tool not found: {tool_id}")
    
    return ToolResponse(
        id=tool.id,
        name=tool.name,
        description=tool.description,
        category=tool.category.value,
        url=tool.url,
        icon=tool.icon,
        tags=tool.tags,
        guide_content=tool.guide_content,
        is_external=tool.is_external
    )

@app.get("/api/categories", response_model=List[CategoryInfo])
async def get_categories():
    """Get all available categories"""
    return [
        CategoryInfo(
            value=cat.value,
            display_name=cat.display_name
        )
        for cat in ToolCategory
    ]

@app.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    """Get statistics about tools"""
    stats = tool_service.get_statistics()
    return StatsResponse(**stats)

@app.get("/api/tags")
async def get_popular_tags(limit: int = 20):
    """Get popular tags"""
    tags = tool_service.get_popular_tags(limit=limit)
    return [{"tag": tag, "count": count} for tag, count in tags]

@app.post("/api/reload")
async def reload_tools():
    """Reload tools from configuration"""
    tool_service.reload_tools()
    return {"message": "Tools reloaded successfully"}

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "tools_count": tool_service.get_tools_count()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
