"""MCP Server initialization and tool registry."""
from typing import Dict, Any, Callable
from backend.mcp_server.tools import (
    create_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task
)
from backend.mcp_server.schemas.tool_definitions import MCP_TOOLS


class MCPServer:
    """MCP Server for managing and executing tools."""

    def __init__(self):
        """Initialize MCP server with tool registry."""
        # Tool function registry
        self.tool_functions: Dict[str, Callable] = {
            "create_task": create_task,
            "list_tasks": list_tasks,
            "complete_task": complete_task,
            "delete_task": delete_task,
            "update_task": update_task,
        }

        # Tool schemas (for Cohere agent)
        self.tool_schemas = MCP_TOOLS

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool by name with provided arguments.

        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments as dictionary

        Returns:
            Tool execution result

        Raises:
            ValueError: If tool not found
        """
        if tool_name not in self.tool_functions:
            return {
                "success": False,
                "error": "invalid_tool",
                "message": f"Tool '{tool_name}' not found"
            }

        tool_func = self.tool_functions[tool_name]

        try:
            result = await tool_func(**arguments)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": "tool_execution_error",
                "message": f"Tool execution failed: {str(e)}"
            }

    def get_tool_schemas(self) -> list:
        """Get all tool schemas for agent initialization."""
        return self.tool_schemas


# Global MCP server instance
mcp_server = MCPServer()
