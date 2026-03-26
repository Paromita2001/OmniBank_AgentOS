# pipeline/llm.py

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

def get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        max_tokens=512,
        api_key=os.getenv("GROQ_API_KEY")  # important
    )
