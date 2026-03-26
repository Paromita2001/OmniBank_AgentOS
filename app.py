# app.py

import os
from graph.builder import build_graph
from db.reminder_db import create_reminder_table
from db.banking_db import (
    create_tables,
    insert_users,
    insert_accounts,
    insert_beneficiaries,
    insert_transactions,
    create_otp_table
)
from services.reminder_scheduler import start_scheduler


# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# -----------------------------
# Create DB + Seed Data
# -----------------------------
# create_tables()
# insert_users()
# insert_accounts()
# insert_beneficiaries()
# insert_transactions()
# create_otp_table()
# create_reminder_table()


create_tables()
create_otp_table()
create_reminder_table()
start_scheduler()

print("OmniBank Agent OS Started")

# -----------------------------
# Start Reminder Scheduler
# -----------------------------
start_scheduler()

# Build graph once at startup
graph = build_graph()


def run_pipeline(user_text: str, user_id: int = 1):
    """
    Main entry point for the system.
    """

    # Initial state
    state = {
        "user_id": user_id,
        "user_query": user_text,
        "intent": None,
        "sub_intent": None,
        "entities": None,
        "result": None
    }

    # Invoke LangGraph
    final_state = graph.invoke(state)

    return final_state.get("result", "❌ No response generated")


# ---------------------------------------
# Simple CLI testing
# ---------------------------------------
if __name__ == "__main__":
    print(" OmniBank Agent OS Started\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        response = run_pipeline(user_input)
        print("Bot:", response)
