# from app_graph.graph_builder import build_graph
# from pipeline import meaning_pipeline
# from pipeline import intent_pipeline
# from pipeline.entity_pipeline import extract_entities
# from app_graph.router import route
# from services.rag_loader import load_or_create_vectorstore


from app_graph.graph_builder import build_graph
from services.rag_loader import load_or_create_vectorstore


# ==================================================
# 1️⃣ LOAD VECTORSTORE (ONCE AT STARTUP)
# ==================================================
vectorstore = load_or_create_vectorstore()


# ==================================================
# 2️⃣ BUILD LANGGRAPH (ONCE)
# ==================================================
graph = build_graph()


def run_pipeline(user_text: str, user_id: int):
    """
    Main orchestration pipeline using LangGraph.
    """

    print("🟡 run_pipeline START")
    print("USER TEXT:", user_text)

    try:
        # ==================================================
        # 3️⃣ INITIAL STATE FOR LANGGRAPH
        # ==================================================
        state = {
            "user_id": user_id,
            "user_query": user_text,
            "vectorstore": vectorstore,
            "intent": None,
            "meaning": None,
            "entities": None,
            "result": None
        }

        # ==================================================
        # 4️⃣ INVOKE LANGGRAPH
        # ==================================================
        final_state = graph.invoke(state)

        print("🟢 FINAL STATE:", final_state)
        print("🟡 run_pipeline END")

        return final_state.get("result", "❌ No response generated")

    except Exception as e:
        print("🔴 ERROR in run_pipeline:", e)
        return "❌ Internal error occurred."
