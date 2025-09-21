# BY MAX
from typing import Annotated

from langchain_core.messages import BaseMessage, AnyMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field


class DeepSearchState ( BaseModel ):
    """
    The overall deep Search Multiagent State
    """
    messages: Annotated [ list [ AnyMessage ], add_messages ] = Field ( default = [], description = "Messages to be sent to tje user." )

    topic_to_search: str = Field ( default = "", description = "The topic the user required to search for" )
    research_brief: str  = Field ( default = "", description = "Research brief generated from user conversation history, a research question that will be used to guide the research" )
    research_result: str = Field ( default = "", description = "The search results" )

    # TODO Altri campi per le varie fasi (subgraphs)...