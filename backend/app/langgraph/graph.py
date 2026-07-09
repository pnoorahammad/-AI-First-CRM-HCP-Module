"""LangGraph compilation and execution."""

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from app.langgraph.state import AgentState
from app.langgraph.nodes import chatbot_node, should_continue, get_tools


from typing import Any


def create_graph(user_id: int) -> Any:
    """Create and compile the LangGraph StateGraph."""

    # Initialize the graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("chatbot", chatbot_node)

    # We create a ToolNode dynamically with the user's tools
    tools = get_tools(user_id)
    tool_node = ToolNode(tools)
    workflow.add_node("tools", tool_node)

    # Add edges
    workflow.add_edge(START, "chatbot")

    workflow.add_conditional_edges(
        "chatbot", should_continue, {"tools": "tools", "__end__": END}
    )

    workflow.add_edge("tools", "chatbot")

    # Compile the graph
    # We could add a checkpointer here for persistence across turns
    # For now, we will pass the full message history per request
    return workflow.compile()
