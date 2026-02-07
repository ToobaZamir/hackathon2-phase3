"""Service for executing Cohere-powered AI agent with MCP tools."""
import json
from typing import List, Dict, Any
from src.agent.cohere_client import CohereClient
from src.agent.system_prompt import SYSTEM_PROMPT
from mcp_server.schemas.tool_definitions import MCP_TOOLS
from mcp_server.server import mcp_server


class AgentService:
    """
    Service for executing Cohere-powered AI agent with MCP tools.

    Stateless design:
    - Fresh client instantiated on each execute() call
    - No instance variables storing conversation state
    - All state passed as parameters or retrieved from DB
    """

    def __init__(self):
        """Initialize agent service (no state stored)."""
        pass

    async def execute(
        self,
        user_id: int,
        message: str,
        history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Execute agent with user message and conversation history.

        Args:
            user_id: ID of the user (for MCP tool calls)
            message: User's new message
            history: Previous conversation messages [{role: str, content: str}]

        Returns:
            {
                "message": str,  # Agent's response
                "tool_calls": List[Dict]  # Tools called during execution
            }
        """
        # 1. Create fresh Cohere client (stateless)
        cohere_client = CohereClient()

        # 2. Build message list
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + history + [
            {"role": "user", "content": message}
        ]

        # 3. Call Cohere API
        try:
            response = cohere_client.chat_completion(
                messages=messages,
                tools=MCP_TOOLS,
                tool_choice="auto",  # Let agent decide when to use tools
                temperature=0.7,
                max_tokens=1000
            )
        except Exception as e:
            return {
                "message": f"I'm having trouble processing your request right now. Please try again. (Error: {str(e)})",
                "tool_calls": None
            }

        # 4. Handle tool calls (if any)
        tool_calls_log = []
        assistant_message = response.choices[0].message

        if assistant_message.tool_calls:
            # Agent wants to call tools
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                # Inject user_id into tool args
                tool_args["user_id"] = user_id

                # Execute tool
                tool_result = await mcp_server.execute_tool(tool_name, tool_args)

                # Log tool call
                tool_calls_log.append({
                    "tool": tool_name,
                    "arguments": tool_args,
                    "result": tool_result
                })

            # Send tool results back to agent for final response
            messages.append({
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in assistant_message.tool_calls
                ]
            })

            # Add tool results as tool role messages
            for i, tool_call in enumerate(assistant_message.tool_calls):
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_calls_log[i]["result"])
                })

            # Get final response from agent
            try:
                final_response = cohere_client.chat_completion(
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000
                )
                final_message = final_response.choices[0].message.content
            except Exception as e:
                # If second call fails, provide helpful error
                final_message = f"I completed the operation but had trouble generating a response. Please check your tasks. (Error: {str(e)})"

        else:
            # No tool calls, use direct response
            final_message = assistant_message.content

        # 5. Return response
        return {
            "message": final_message,
            "tool_calls": tool_calls_log if tool_calls_log else None
        }
