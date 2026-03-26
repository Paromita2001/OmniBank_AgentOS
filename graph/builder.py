from langgraph.graph import StateGraph, END
from graph.state import GraphState
from graph.nodes import (
    intent_node,
    bank_node,
    reminder_node,
    rag_node,
    fallback_node,
    analytics_node
)


def build_graph():
    """
    Builds the LangGraph execution flow.
    """

    builder = StateGraph(GraphState)

    # -----------------------------
    # Add Nodes
    # -----------------------------
    builder.add_node("intent_node", intent_node)
    builder.add_node("bank_node", bank_node)
    builder.add_node("reminder_node", reminder_node)
    builder.add_node("rag_node", rag_node)
    builder.add_node("fallback_node", fallback_node)
    builder.add_node("analytics_node", analytics_node)

    # -----------------------------
    # Entry Point
    # -----------------------------
    builder.set_entry_point("intent_node")

    # -----------------------------
    # Routing Logic
    # -----------------------------
    def route_by_intent(state: GraphState):

        intent = state.get("intent")

        # -----------------
        # Banking
        # -----------------
        if intent == "banking":
            return "bank_node"

        # -----------------
        # Reminder
        # -----------------
        if intent == "reminder":
            return "reminder_node"

        # -----------------
        # Analytics
        # -----------------
        if intent == "analytics":
            return "analytics_node"

        # -----------------
        # Informational (RAG)
        # -----------------
        if intent == "information":
            return "rag_node"

        # -----------------
        # Fallback
        # -----------------
        return "fallback_node"

    builder.add_conditional_edges(
        "intent_node",
        route_by_intent
    )

    # -----------------------------
    # End Edges
    # -----------------------------
    builder.add_edge("bank_node", END)
    builder.add_edge("reminder_node", END)
    builder.add_edge("rag_node", END)
    builder.add_edge("fallback_node", END)
    builder.add_edge("analytics_node", END)

    return builder.compile()

app_graph = build_graph()