from typing import Annotated, Optional

from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, AnyMessage
from langgraph.graph import add_messages



class PlannerAgentState ( BaseModel):

    """
    State for the Planner Agent
    """
    messages: Annotated [ list [ AnyMessage ], add_messages ] = Field ( default = [], description = "Messages to be sent to the user" )
    need_clarification: bool              = Field ( default = False, description = "Whether the user needs to be asked a clarifying question" )
    question: Optional [ str ]           = Field ( default = None, description = "A question to ask the user to clarify the report scope" )
    verification: Optional [ str ]        = Field ( default = None, description = "Verify message that we will start research after the user has provided the necessary information" )
    research_brief: Optional [ str]      = Field ( default = None, description = "The phrase describing the topic to be searched and what aspects to be considered during the search" )



# This state class is used to let the model generate a ToolCall that we use to interrupt the graph and ask the user for a clarification
class AskHuman ( BaseModel ):

    """
    Ask the human a question
    """

    question: str = Field ( description = "The question to be asked to the user as clarification" )
