# pipeline/schema.py

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
