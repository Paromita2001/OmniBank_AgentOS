# pipeline/schema.py

from pydantic import BaseModel, Field
from typing import Dict, Any, Literal


class IntentOutput(BaseModel):
    """
    Structured output returned by LLM.
    """

    intent: Literal[
        "bank_action",
        "reminder",
        "analytics",
        "info",
        "fallback"
    ] = Field(
        description="Main intent category"
    )

    sub_intent: Literal[
        "balance_check",
        "transaction_history",
        "money_transfer",
        "spending_analysis",
        "add_reminder",
        "view_reminder",
        "unknown"
    ] = Field(
        description="Specific action under main intent"
    )

    entities: Dict[str, Any] = Field(
        default_factory=dict,
        description="Extracted structured entities like timeframe, amount, receiver"
    )
from pydantic import BaseModel
from typing import Optional, Dict, Any


class TimeEntity(BaseModel):
    type: str              # relative | absolute
    unit: Optional[str]    # days | months | hours
    value: Optional[int]   # 2, 3 etc
    text: Optional[str]    # "march", "last month"


class IntentOutput(BaseModel):
    intent: str
    sub_intent: str
    entities: Dict[str, Any]
