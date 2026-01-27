# pipeline/intent_parser.py

from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pipeline.llm import get_llm
import re


# ---------- Output Schema ----------
class IntentOutput(BaseModel):
    intent: str = Field(
        description="High level intent like bank_action, reminder, info"
    )
    sub_intent: str = Field(
        description="Specific action like transaction_history, balance_check, money_transfer"
    )
    entities: dict = Field(
        default_factory=dict,
        description="Extracted entities like time range, amount, receiver"
    )


# ---------- Parser ----------
parser = PydanticOutputParser(pydantic_object=IntentOutput)


# ---------- Prompt ----------
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an intent extraction engine for a banking assistant.

You MUST return JSON strictly in this format:
{format_instructions}

Rules:
- intent must be one of: bank_action, reminder, info, fallback
- sub_intent must be one of:
  - transaction_history
  - balance_check
  - money_transfer
  - spending_analysis
  - unknown

Entity extraction rules:
- If user asks for "last N transactions", extract:
  entities.count = N
- If user asks for time-based queries, extract:
  entities.timeframe
- entities can include:
  - timeframe
  - count
  - amount
  - receiver
"""
    ),
    ("human", "{user_input}")
])


# ---------- Chain ----------
chain = prompt | get_llm() | parser


# ---------- Main Function ----------
def parse_intent(user_input: str) -> IntentOutput:
    user_input = user_input.strip()

    # 🔐 HARD OTP OVERRIDE (NO LLM)
    if re.fullmatch(r"\d{4,6}", user_input):
        return IntentOutput(
            intent="bank_action",
            sub_intent="money_transfer",
            entities={"otp": user_input}
        )

    # 🤖 LLM-based intent parsing
    return chain.invoke({
        "user_input": user_input,
        "format_instructions": parser.get_format_instructions()
    })
