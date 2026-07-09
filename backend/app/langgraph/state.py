"""State definition for the LangGraph agent."""

from typing import TypedDict, List, Dict, Any, Optional
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """The state of the conversation graph."""

    # Core conversation state
    messages: List[BaseMessage]

    # Extracted entity data for preview
    extracted_data: Optional[Dict[str, Any]]

    # State tracking
    current_step: str

    # Session metadata
    user_id: int
    session_id: str

    # Validation results
    validation_errors: List[str]
    is_valid: bool

    # Final confirmed payload ready for DB saving
    final_payload: Optional[Dict[str, Any]]
