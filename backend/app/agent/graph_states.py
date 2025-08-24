"""BatLabs Graph States"""

from typing import Literal, Optional

from langgraph.graph import MessagesState
from pydantic import BaseModel


class OverallState(MessagesState):
    """Represents the state of the graph for a specific query."""

    query: str
    message_type: Literal["text", "file"]
    file_content: Optional[str]


class UserData(BaseModel):
    """Semantic Memory Data Model"""

    name: str
    preferences: dict
    habits: list[str]
    communication_style: str
    contacts: list[str]
    health_data: dict
    goal_related_data: dict
