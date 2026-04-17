# # pipeline/llm.py

# import os
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq

# # Load environment variables
# #load_dotenv()

# from dotenv import load_dotenv
# from pathlib import Path
# import os

# # ✅ FORCE load .env from root
# load_dotenv(Path(__file__).parent.parent / ".env")

# def get_llm():
#     return ChatGroq(
#         model="llama-3.1-8b-instant",
#         temperature=0,
#         max_tokens=512,
#         api_key=os.getenv("GROQ_API_KEY")  # important
#     )
    


import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_groq import ChatGroq

# ✅ Load .env properly
load_dotenv(Path(__file__).parent.parent / ".env")

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    

    if not api_key:
        raise ValueError("❌ GROQ_API_KEY not found!")
    # ✅ Debug check
    print("DEBUG KEY:", api_key[:10] if api_key else "NOT FOUND")

    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        max_tokens=512,
        api_key=api_key
    )