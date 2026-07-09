"""LangGraph Nodes for the Conversation Agent."""

from typing import Dict, Any, List
from langchain_core.messages import SystemMessage

from app.langgraph.state import AgentState
from app.langgraph.llm import get_llm
from app.tools.search_hcp import SearchHCPTool
from app.tools.interaction_summary import InteractionSummaryTool
from app.tools.followup_recommendation import FollowupRecommendationTool
from app.tools.log_interaction import LogInteractionTool
from app.tools.edit_interaction import EditInteractionTool

# System prompt to guide the AI
SYSTEM_PROMPT = """You are a highly capable AI assistant for a Life Sciences CRM.
Your primary goal is to help field representatives log their interactions with Healthcare Professionals (HCPs).
You can understand natural language descriptions of meetings and extract structured data.
You have access to several tools:
- search_hcp: To find the ID of a doctor if the user hasn't provided it.
- interaction_summary: To pull up past meeting notes.
- followup_recommendation: To get suggestions for next steps.
- log_interaction: To save the finalized interaction data to the database.

When the user describes a meeting:
1. Identify the HCP (use search_hcp if needed).
2. Extract the date, time (default to current if missing), visit type, products discussed, samples given, feedback, and notes.
3. Show the user a summary of what you understood and ask for confirmation before saving.
4. Only call log_interaction when the user explicitly confirms the details are correct.
"""


def get_tools(user_id: int) -> List[Any]:
    """Initialize tools with the current user's context."""
    return [
        SearchHCPTool(),
        InteractionSummaryTool(user_id=user_id),
        FollowupRecommendationTool(user_id=user_id),
        LogInteractionTool(user_id=user_id),
        EditInteractionTool(user_id=user_id),
    ]


def chatbot_node(state: AgentState) -> Dict[str, Any]:
    """The main LLM node that decides what to do next."""
    messages = state["messages"]
    user_id = state.get("user_id")

    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    llm = get_llm()
    tools = get_tools(user_id)
    llm_with_tools = llm.bind_tools(tools)

    response = llm_with_tools.invoke(messages)

    return {"messages": [response], "current_step": "chatbot"}


def should_continue(state: AgentState) -> str:
    """Determine whether to use tools or end."""
    messages = state["messages"]
    last_message = messages[-1]

    if getattr(last_message, "tool_calls", None):
        return "tools"
    return "__end__"
