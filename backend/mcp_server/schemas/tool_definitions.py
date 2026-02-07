"""Cohere-compatible tool schema definitions for MCP tools."""

# Tool schemas in OpenAI function calling format (Cohere-compatible)
MCP_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Creates a new task for the user. Use this when the user wants to add, create, or be reminded of something.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user creating the task (from JWT token)"
                    },
                    "title": {
                        "type": "string",
                        "description": "The task title (1-255 characters)",
                        "minLength": 1,
                        "maxLength": 255
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional detailed description of the task",
                        "maxLength": 1000
                    }
                },
                "required": ["user_id", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Retrieves tasks for the user. Supports filtering by completion status. Use this when the user wants to see, show, or list their tasks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user (from JWT token)"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter tasks by status (default: all)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of tasks to return (default: 50)",
                        "minimum": 1,
                        "maximum": 100
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Number of tasks to skip for pagination (default: 0)",
                        "minimum": 0
                    }
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Updates an existing task's title, description, or status. Use this when the user wants to change, update, modify, or edit a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user (from JWT token)"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New task title (1-255 characters)",
                        "minLength": 1,
                        "maxLength": 255
                    },
                    "description": {
                        "type": "string",
                        "description": "New task description",
                        "maxLength": 1000
                    },
                    "completed": {
                        "type": "boolean",
                        "description": "New completion status (true = completed, false = pending)"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Permanently deletes a task. Use this when the user wants to delete or remove a task. Always confirm before calling this tool.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user (from JWT token)"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to delete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Marks a task as completed. This is a shortcut for update_task with completed=true. Use when the user says they finished, completed, or are done with a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user (from JWT token)"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to mark as complete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        }
    }
]
