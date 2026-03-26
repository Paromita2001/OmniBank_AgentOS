# # pipeline/intent_parser.py

# from pydantic import BaseModel, Field
# from langchain_core.output_parsers import PydanticOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from pipeline.llm import get_llm
# import re


# # ---------- Output Schema ----------
# class IntentOutput(BaseModel):
#     intent: str = Field(
#         description="One of: banking, reminder, analytics, information, other"
#     )
#     sub_intent: str = Field(
#         description="Specific action like transaction_history, balance_check, money_transfer, spending_analysis, unknown"
#     )
#     actionable: bool = Field(
#         description="True only if this requires execution in DB. False for informational queries."
#     )
#     entities: dict = Field(
#         default_factory=dict,
#         description="Extracted entities like time range, amount, receiver, phone_number, otp"
#     )



# # ---------- Parser ----------
# parser = PydanticOutputParser(pydantic_object=IntentOutput)


# # ---------- Prompt ----------
# prompt = ChatPromptTemplate.from_messages([
#     (
#         "system",
#         """
# You are an intent extraction engine for a banking assistant.

# You MUST return JSON strictly in this format:
# {format_instructions}

# Rules:
# - intent must be one of:
#   - banking
#   - reminder
#   - analytics
#   - information
#   - other

# - sub_intent must be one of:
#   - transaction_history
#   - balance_check
#   - money_transfer
#   - spending_analysis
#   - unknown

# Entity extraction rules:
# - If user asks for "last N transactions", extract:
#   entities.count = N
# - If user asks for time-based queries, extract:
#   entities.timeframe
# - entities can include:
#   - timeframe
#   - count
#   - amount
#   - receiver

# Actionable rules:

# - balance_check is actionable ONLY if user refers to their own account (e.g. "my balance").
# - money_transfer is actionable ONLY if amount AND receiver/phone_number are present.
# - transaction_history is actionable.
# - spending_analysis is actionable.
# - If the query is informational (e.g. "What is transfer limit?"), set actionable = false.


# If user provides a 10-digit phone number,
# extract it as:
# entities.phone_number

# If user wants to set a reminder:

# intent = reminder
# sub_intent = add_reminder

# Extract the following entities:

# - task (what to do)
# - date (if specific date mentioned)
# - time (if mentioned)
# - frequency (one of: daily, weekly, monthly, yearly, one_time)

# Frequency rules:
# - "every day" → daily
# - "every week" or weekday like Monday → weekly
# - "every month" or "2nd every month" → monthly
# - "every year" or "every 15 August" → yearly
# - specific date only → one_time
# """
#     ),
#     ("human", "{user_input}")
# ])


# # ---------- Chain ----------
# chain = prompt | get_llm() | parser


# # ---------- Main Function ----------
# def parse_intent(user_input: str) -> IntentOutput:
#     user_input = user_input.strip()

#     # 🔐 HARD OTP OVERRIDE (NO LLM)
#     if re.fullmatch(r"\d{4,6}", user_input):
#         return IntentOutput(
#             intent="banking",
#             sub_intent="money_transfer",
#             actionable=True,
#             entities={"otp": user_input}
#         )


#     # 🤖 LLM-based intent parsing
#     result = chain.invoke({
#         "user_input": user_input,
#         "format_instructions": parser.get_format_instructions()
#     })

#     # 🔁 Normalize intent based on sub_intent
#     if result.sub_intent in ["balance_check", "money_transfer", "transaction_history"]:
#         result.intent = "banking"

#     if result.sub_intent == "spending_analysis":
#         result.intent = "analytics"

#     # If not actionable → force informational
#     if result.actionable is False and result.intent == "banking":
#         result.intent = "information"

#     return result






# pipeline/intent_parser.py

from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pipeline.llm import get_llm
import re


# ---------- Output Schema ----------
class IntentOutput(BaseModel):
    intent: str = Field(
        description="One of: banking, reminder, analytics, information, fallback"
    )
    sub_intent: str = Field(
        description="transaction_history, balance_check, money_transfer, spending_analysis, add_reminder, unknown"
    )
    actionable: bool = Field(
        description="True only if this requires execution in DB."
    )
    entities: dict = Field(
        default_factory=dict
    )


parser = PydanticOutputParser(pydantic_object=IntentOutput)


# ---------- Prompt ----------
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
"""
You are an intent extraction engine for a banking assistant.

You MUST return JSON strictly in this format:
{format_instructions}

Allowed intents:
- banking
- reminder
- analytics
- information
- other

Allowed sub_intents:
- transaction_history
- balance_check
- money_transfer
- spending_analysis
- add_reminder
- show_reminders
- delete_reminder
- unknown

--------------------------------
BANKING RULES
--------------------------------
If user asks:

- "my balance" → 
  intent = banking
  sub_intent = balance_check
  actionable = true

- "send / transfer" →
  intent = banking
  sub_intent = money_transfer
  actionable = true

- "last N transactions" →
  intent = banking
  sub_intent = transaction_history
  actionable = true
  extract:
    entities.count = N

If user provides a 10-digit phone number:
  extract entities.phone_number

Extract:
- amount
- receiver
- phone_number

--------------------------------
ANALYTICS RULES
--------------------------------
If user asks about spending (e.g. spend, spent, spending):

intent = analytics
sub_intent = spending_analysis
actionable = true

You MUST extract:

- category (if mentioned)
- timeframe (MANDATORY)

Timeframe extraction rules:

- "last month" → last_month
- "this month" → this_month
- "last week" → last_week
- "today" → today

If timeframe is clearly mentioned in text,
you MUST include it in entities.timeframe.
Never leave timeframe empty if mentioned.

-----------------------------
REMINDER RULES
-----------------------------

If user says:
- "set reminder"
- "remind me"
- "create reminder"

Then:
intent = reminder
sub_intent = add_reminder
actionable = true

Extract:
- task
- date (if mentioned)
- time (if mentioned)
- frequency (daily, weekly, monthly, yearly, one_time)


If user says:
- "show reminders"
- "show my reminders"
- "list reminders"

Then:
intent = reminder
sub_intent = show_reminders
actionable = true


If user says:
- delete reminder
- remove reminder
- delete this reminder

Then:
intent = reminder
sub_intent = delete_reminder
actionable = true

Extract:
- task (if mentioned)
- date (if mentioned)

--------------------------------
INFORMATION RULES
--------------------------------
If user asks general banking info
(e.g. "What is KYC?", "What is transfer limit?"):

intent = information
sub_intent = unknown
actionable = false

--------------------------------
OTHER
--------------------------------
If unrelated or open-domain:
intent = other
actionable = false

Return ONLY valid JSON.
Do not explain anything.
Do not add extra text.
"""
    ),
    ("human", "{user_input}")
])


chain = prompt | get_llm() | parser


# ---------- Main ----------
def parse_intent(user_input: str) -> IntentOutput:
    user_input = user_input.strip()

    # 🔐 OTP HARD OVERRIDE
    if re.fullmatch(r"\d{4,6}", user_input):
        return IntentOutput(
            intent="banking",
            sub_intent="money_transfer",
            actionable=True,
            entities={"otp": user_input}
        )

    result = chain.invoke({
        "user_input": user_input,
        "format_instructions": parser.get_format_instructions()
    })

    # ---------- Normalization ----------

    if result.sub_intent in [
        "balance_check",
        "money_transfer",
        "transaction_history"
    ]:
        result.intent = "banking"

    if result.sub_intent in [
        "add_reminder", 
        "show_reminders", 
        "delete_reminder"
    ]:
        result.intent = "reminder"

    if result.sub_intent == "spending_analysis":
        result.intent = "analytics"

    if result.sub_intent == "add_reminder":
        result.intent = "reminder"
        result.actionable = True

    # Force fallback safety
    if result.intent not in [
        "banking", "reminder", "analytics", "information", "fallback"
    ]:
        result.intent = "fallback"

    return result