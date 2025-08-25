from typing import Annotated, Optional

from pydantic import BaseModel, Field
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages



class PlannerAgentState ( BaseModel):

    """
    State for the Planner Agent
    """
    messages: Annotated [ list [ AnyMessage ], add_messages ] = Field ( default = [], description = "Messages to be sent to tje user." )
    need_clarification: bool              = Field ( default = False, description = "Whether the user needs to be asked a clarifying question." )
    question: Optional [ str ]           = Field ( default = None, description = "A question to ask the user to clarify the report scope." )
    verification: Optional [ str ]        = Field ( default = None, description = "Verify message that we will start research after the user has provided the necessary information." )
