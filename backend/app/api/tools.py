"""Tools API endpoints."""

from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.models.user import User
from app.langgraph.nodes import get_tools

router = APIRouter(prefix="/api/tools", tags=["Tools"])


@router.get("/")
def list_available_tools(current_user: User = Depends(get_current_user)):
    """List all available AI tools for the current user."""
    tools = get_tools(current_user.id)
    return {
        "tools": [
            {
                "name": tool.name,
                "description": tool.description,
            }
            for tool in tools
        ]
    }
