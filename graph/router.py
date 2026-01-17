# app_graph/router.py

from services import rag_handler
from agents.bank_agent import BankAgent
from agents.reminder_agent import handle as reminder_agent
from agents.fallback_agent import handle as fallback_agent

# Single instance (important for OTP / DB consistency)
bank_agent = BankAgent()


def route(
    *,
    user_id: int,
    intent: dict,
    context: str,
    meaning: dict | None = None,
    entities: dict | None = None
):
    """
    Central router that sends request to the correct handler.
    """

    main_intent = intent.get("intent")
    entities = entities or {}

    # =========================
    # 1️⃣ BANK ACTIONS
    # =========================
    if main_intent == "bank_action":
        return bank_agent.handle(
            user_id=user_id,
            intent=intent,
            entities=entities
        )

    # =========================
    # 2️⃣ INFORMATIONAL (RAG → LLM fallback)
    # =========================
    if main_intent == "info":
        return rag_handler.handle(
            context=context,
            meaning=meaning
        )

    # =========================
    # 3️⃣ REMINDERS
    # =========================
    if main_intent == "reminder":
        return reminder_agent(
            context=context,
            user_id=user_id,
            intent=intent
        )

    # =========================
    # 4️⃣ FINAL FALLBACK
    # =========================
    return fallback_agent(context)
