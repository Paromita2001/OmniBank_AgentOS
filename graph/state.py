# graph/state.py

from typing import TypedDict, Optional, Dict, Any


class GraphState(TypedDict):
    """
    Shared state that moves across LangGraph nodes.
    """

    user_id: int
    user_query: str

    # Filled by Intent Node
    # Filled by Intent Node
    intent: Optional[str]
    sub_intent: Optional[str]
    actionable: Optional[bool]
    entities: Optional[Dict[str, Any]]

    # Filled by Agent Node
    result: Optional[str]
