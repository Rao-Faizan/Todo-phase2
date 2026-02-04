"""Chat API endpoint for AI-powered todo management"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Dict, Any, Optional
from uuid import UUID
from sqlmodel import Session
from database import get_session
from services.ai.agent_service import agent_service
from middleware.user_validation import get_current_user
from pydantic import BaseModel
import json


router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: UUID
    message_id: Optional[UUID] = None


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    token_data: dict = Depends(get_current_user),
    request: ChatRequest = None,
    session: Session = Depends(get_session)
):
    """
    Main chat endpoint for AI-powered todo management
    Accepts user messages and returns AI responses using OpenAI and MCP tools
    """
    # Extract user ID from token
    user_id = UUID(token_data.get("sub"))
    try:
        # Process the message through the AI agent
        result = await agent_service.process_message(
            user_id=user_id,
            message_content=request.message,
            conversation_id=request.conversation_id,
            session=session
        )

        return ChatResponse(
            response=result["response"],
            conversation_id=result["conversation_id"],
            message_id=result.get("message_id")
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Chat endpoint error: {str(e)}")

        # Return a user-friendly error message
        raise HTTPException(
            status_code=500,
            detail="Sorry, I encountered an error processing your request. Please try again."
        )


# Additional endpoints for conversation management

@router.get("/conversations")
async def get_user_conversations(
    token_data: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all conversations for a user"""
    # Extract user ID from token
    user_id = UUID(token_data.get("sub"))

    try:
        from services.conversation_history_service import conversation_history_service

        conversations = await conversation_history_service.get_user_conversations(
            user_id=user_id,
            session=session
        )

        return {"conversations": conversations}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving conversations: {str(e)}"
        )


@router.get("/conversations/{conversation_id}")
async def get_conversation_history(
    conversation_id: UUID,
    token_data: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get specific conversation history"""
    # Extract user ID from token
    user_id = UUID(token_data.get("sub"))

    try:
        from services.conversation_history_service import conversation_history_service

        # Verify user owns this conversation
        conversation = await conversation_history_service.get_conversation_by_id(
            conversation_id=conversation_id,
            user_id=user_id,
            session=session
        )

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        messages = await conversation_history_service.get_conversation_messages(
            conversation_id=conversation_id,
            session=session
        )

        return {
            "conversation_id": conversation_id,
            "messages": messages
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving conversation: {str(e)}"
        )