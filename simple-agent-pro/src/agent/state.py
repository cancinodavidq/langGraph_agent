from typing import Optional, List, TypedDict

class AgentState(TypedDict):
    messages: List
    error: Optional[str]
