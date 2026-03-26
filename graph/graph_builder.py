# app_graph/graph_builder.py

from pipeline.context_pipeline import build_context
from pipeline.meaning_pipeline import run as meaning_pipeline
from pipeline.intent_pipeline import run as intent_pipeline
from pipeline.entity_pipeline import extract_entities
from pipeline.input_router import is_direct_bank_command
from app_graph.router import route


class SimpleGraph:
    """
    Central execution graph for Omni BankPilot
    """

    def invoke(self, data: dict) -> dict:
        """
        data example:
        {
            "input": "send 500 to Rohit Sharma",
            "user_id": 1
        }
        """

        user_input: str = data["input"]
        user_id: int = data["user_id"]

        # =========================
        # 1️⃣ Context Layer
        # =========================
        context = build_context(user_input, history=[])

        # =========================
        # 2️⃣ Meaning Layer
        # IMPORTANT: Skip LLM if direct bank command
        # =========================
        if is_direct_bank_command(user_input):
            meaning = {
                "action": "transfer" if "send" in user_input.lower() else "check",
                "object": "money" if "send" in user_input.lower() else "balance",
                "owner": "self"
            }
        else:
            meaning = meaning_pipeline(user_input)

        # =========================
        # 3️⃣ Entity Extraction
        # =========================
        entities = extract_entities(user_input, meaning)

        # =========================
        # 4️⃣ Intent Detection
        # =========================
        intent = intent_pipeline(meaning)

        # =========================
        # 5️⃣ Routing
        # =========================
        response = route(
            user_id=user_id,
            intent=intent,
            context=context,
            meaning=meaning,
            entities=entities
        )

        return {"response": response}


def build_graph():
    """
    Factory method
    """
    return SimpleGraph()
