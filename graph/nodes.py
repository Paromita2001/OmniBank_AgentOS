# graph/nodes.py

from graph.state import GraphState
from pipeline.intent_parser import parse_intent
from agents.bank_agent import BankAgent
from agents.reminder_agent import ReminderAgent
from agents.rag_agent import RAGAgent
from agents.fallback_agent import FallbackAgent
from agents.analytics_agent import AnalyticsAgent
from db.banking_db import get_otp


# Single instances (important)
bank_agent = BankAgent()
reminder_agent = ReminderAgent()
rag_agent = RAGAgent()
fallback_agent = FallbackAgent()
analytics_agent = AnalyticsAgent()


# ==============================
# 1️⃣ INTENT NODE
# ==============================
def intent_node(state: GraphState) -> GraphState:
    """
    Fully LLM-based intent detection with OTP override.
    """

    user_query = state["user_query"]
    user_id = state["user_id"]

    # ---------------------------------
    # OTP OVERRIDE
    # ---------------------------------
    record = get_otp(user_id)

    if record:
        saved_otp, receiver, phone_number, amount, category, created_at = record

        # If user entering OTP
        if user_query.strip().isdigit():
            state["intent"] = "banking"
            state["sub_intent"] = "money_transfer"
            state["entities"] = {"otp": user_query.strip()}
            return state

        # If category not yet provided
        if category == "PENDING":
            state["intent"] = "banking"
            state["sub_intent"] = "money_transfer"
            state["entities"] = {"category": user_query}
            return state
    # ---------------------------------
    # LLM Parsing
    # ---------------------------------
    parsed = parse_intent(user_query)

    allowed_intents = [
        "banking",
        "reminder",
        "analytics",
        "information",
        "fallback"
    ]

    if parsed.intent not in allowed_intents:
        state["intent"] = "fallback"
        state["sub_intent"] = None
        state["entities"] = {}
        return state

    state["intent"] = parsed.intent
    state["sub_intent"] = parsed.sub_intent
    state["entities"] = parsed.entities or {}

    return state


# ==============================
# 2️⃣ BANK NODE
# ==============================
def bank_node(state: GraphState) -> GraphState:

    response = bank_agent.handle(
        user_id=state["user_id"],
        intent={
            "sub_intent": state["sub_intent"],
            "raw_input": state["user_query"]   # 👈 ADD THIS
        },
        entities=state["entities"]
    )

    state["result"] = response
    return state


# ==============================
# 3️⃣ REMINDER NODE
# ==============================
def reminder_node(state: GraphState) -> GraphState:
    
    print("DEBUG REMINDER INTENT:", state["sub_intent"])
    print("DEBUG REMINDER ENTITIES:", state["entities"])
    
    response = reminder_agent.handle(
        user_id=state["user_id"],
        intent={"sub_intent": state["sub_intent"]},
        entities=state["entities"]
    )

    state["result"] = response
    return state


# ==============================
# 4️⃣ RAG NODE
# ==============================
def rag_node(state: GraphState) -> GraphState:
    """
    Informational banking queries via RAG.
    Falls back to LLM if weak match.
    """

    response = rag_agent.handle(
        query=state["user_query"]
    )

    # If RAG fails → fallback
    if not response or "could not find" in response.lower():
        return fallback_node(state)

    state["result"] = response
    return state


# ==============================
# 5️⃣ FALLBACK NODE
# ==============================
def fallback_node(state: GraphState) -> GraphState:
    """
    Open-domain LLM answers.
    """

    # Important: NO keyword argument
    response = fallback_agent.handle(
        state["user_query"]
    )

    state["result"] = response
    return state


# ==============================
# 6️⃣ ANALYTICS NODE
# ==============================
def analytics_node(state: GraphState) -> GraphState:

    print("DEBUG ANALYTICS ENTITIES:", state["entities"])

    response = analytics_agent.handle(
        user_id=state["user_id"],
        intent={
            "sub_intent": state["sub_intent"]
        },
        entities=state["entities"]
    )

    state["result"] = response
    return state



