"""Cohere client wrapper using OpenAI SDK compatibility."""
from openai import OpenAI
from typing import List, Dict, Any, Optional
import os
from backend.src.core.config import settings


class CohereClient:
    """
    Wrapper for Cohere API using OpenAI SDK compatibility endpoint.

    This allows us to use the familiar OpenAI SDK interface while
    leveraging Cohere's command-a-03-2025 model for tool calling.
    """

    def __init__(self):
        """Initialize Cohere client with OpenAI SDK compatibility."""
        self.api_key = settings.cohere_api_key
        if not self.api_key:
            raise ValueError("COHERE_API_KEY environment variable not set")

        self.model = settings.cohere_model
        self.base_url = settings.cohere_base_url

        # Create OpenAI client configured for Cohere
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: str = "auto",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ):
        """
        Create a chat completion using Cohere via OpenAI SDK.

        Args:
            messages: List of message dictionaries with role and content
            tools: Optional list of tool definitions
            tool_choice: How the model should choose tools ("auto", "none", or specific tool)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response

        Returns:
            OpenAI chat completion response object
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice=tool_choice,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response
        except Exception as e:
            # Log error and re-raise with context
            raise RuntimeError(f"Cohere API call failed: {str(e)}") from e

    def close(self):
        """Close the client connection (if needed)."""
        # OpenAI client doesn't require explicit closing
        pass
