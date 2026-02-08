"""Service that orchestrates the full chatbot conversation cycle.

Responsibilities
────────────────
1. Load conversation history from the database.
2. Persist the incoming user message.
3. Call the AI agent (Cohere via AgentService) with the full history.
4. Persist the AI response.
5. Return a structured result to the caller.

Every public method receives only primitive IDs and strings so the
router stays thin and this service remains easy to test.
"""
import logging
from typing import Any, Dict, List, Optional

from sqlmodel import Session

from src.models.message import Message
from src.services.conversation_service import ConversationService
from src.services.agent_service import AgentService

logger = logging.getLogger(__name__)


class ChatbotService:
    """Orchestrates a single user ↔ AI exchange inside a conversation."""

    def __init__(self, session: Session):
        self.conversation_service = ConversationService(session)
        self.agent_service = AgentService()

    # ── public API ──────────────────────────────────────────────

    async def handle_message(
        self,
        conversation_id: int,
        user_id: int,
        user_message: str,
    ) -> Dict[str, Any]:
        """Run the full chat cycle and return the result.

        Args:
            conversation_id: Existing conversation the message belongs to.
            user_id:         Owner of the conversation (passed to MCP tools).
            user_message:    Plain-text message from the user.

        Returns:
            {
                "conversation_id": int,
                "user_message":    Message,   # persisted user row
                "ai_message":      Message,   # persisted AI row
                "ai_response":     str,       # the text the AI produced
            }

        Raises:
            RuntimeError: If the AI agent fails after the user message has
                          already been saved (the user row is *not* rolled
                          back so the conversation stays consistent).
        """
        # 1. Fetch existing conversation history for context
        history: List[Dict[str, str]] = (
            self.conversation_service.get_conversation_history(conversation_id)
        )

        # 2. Persist user message *before* calling the AI so the DB
        #    always reflects what the user actually sent, even if the
        #    agent call fails later.
        saved_user_msg: Message = self.conversation_service.add_message(
            conversation_id=conversation_id,
            sender="user",
            content=user_message,
        )
        logger.info(
            "Saved user message %s in conversation %s",
            saved_user_msg.id,
            conversation_id,
        )

        # 3. Call the AI agent with full history + new message
        ai_result = await self._call_agent(
            user_id=user_id,
            message=user_message,
            history=history,
        )
        ai_response_text: str = ai_result["message"]

        # 4. Persist AI response
        saved_ai_msg: Message = self.conversation_service.add_message(
            conversation_id=conversation_id,
            sender="ai",
            content=ai_response_text,
        )
        logger.info(
            "Saved AI message %s in conversation %s",
            saved_ai_msg.id,
            conversation_id,
        )

        # 5. Return structured result
        return {
            "conversation_id": conversation_id,
            "user_message": saved_user_msg,
            "ai_message": saved_ai_msg,
            "ai_response": ai_response_text,
        }

    # ── internals ───────────────────────────────────────────────

    async def _call_agent(
        self,
        user_id: int,
        message: str,
        history: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        """Delegate to AgentService and translate failures.

        Returns:
            Raw dict from AgentService:
            {"message": str, "tool_calls": list | None}

        Raises:
            RuntimeError: On any agent / API failure.
        """
        try:
            return await self.agent_service.execute(
                user_id=user_id,
                message=message,
                history=history,
            )
        except Exception as exc:
            logger.exception("Agent execution failed for user %s", user_id)
            raise RuntimeError(f"AI agent failed: {exc}") from exc
