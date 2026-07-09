"""Business logic for Chat and LangGraph orchestration."""

import time
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from app.models.ai_log import AILog
from app.langgraph.graph import create_graph


def process_chat_message(
    db: Session,
    user_id: int,
    session_id: str,
    message: str,
    history: List[Dict[str, str]],
) -> Dict[str, Any]:
    """Process a user message through the LangGraph agent."""
    start_time = time.time()

    # Reconstruct message history for LangChain
    langchain_messages = []
    for msg in history:
        if msg["role"] == "user":
            langchain_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            langchain_messages.append(AIMessage(content=msg["content"]))

    # Add current message
    langchain_messages.append(HumanMessage(content=message))

    # Initialize state
    initial_state = {
        "messages": langchain_messages,
        "user_id": user_id,
        "session_id": session_id,
        "current_step": "init",
    }

    # Run graph
    graph = create_graph(user_id)
    final_state = graph.invoke(initial_state)

    # Extract final response
    final_messages = final_state["messages"]
    last_message = final_messages[-1]

    response_content = last_message.content
    if (
        not response_content
        and hasattr(last_message, "tool_calls")
        and last_message.tool_calls
    ):
        # If the last message was a tool call (shouldn't happen with our current graph ending on chatbot, but just in case)
        response_content = "I'm processing that for you..."

    # Calculate metrics
    latency_ms = int((time.time() - start_time) * 1000)

    # Find tools used in this run
    tools_used = []
    for msg in final_messages[len(langchain_messages) :]:
        if isinstance(msg, ToolMessage):
            tools_used.append(msg.name)

    tools_str = ",".join(tools_used) if tools_used else None

    # Log to database
    ai_log = AILog(
        user_id=user_id,
        session_id=session_id,
        input_text=message,
        output_text=response_content,
        tool_used=tools_str,
        latency_ms=latency_ms,
    )
    db.add(ai_log)
    db.commit()

    return {
        "response": response_content,
        "tools_used": tools_used,
        "session_id": session_id,
    }


def get_chat_history(db: Session, user_id: int, session_id: str) -> List[AILog]:
    """Get the chat history for a specific session."""
    return (
        db.query(AILog)
        .filter(AILog.user_id == user_id, AILog.session_id == session_id)
        .order_by(AILog.created_at)
        .all()
    )
