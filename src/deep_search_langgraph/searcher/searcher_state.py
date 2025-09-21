import operator
from typing import Annotated, Sequence, List, TypedDict

from langchain_core.messages import BaseMessage, AnyMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field


class ResearcherState ( BaseModel ):
    """
    State for the research agent containing message history and research metadata.

    This state tracks the researcher's conversation, iteration count for limiting
    tool calls, the research topic being investigated, compressed findings,
    and raw research notes for detailed analysis.
    """
    researcher_messages: Annotated [ Sequence [ AnyMessage ], add_messages ] = Field ( default = [], description = "Messages to be sent to the user" )
    tool_call_iterations: int                                                = Field ( default = 0, description = "Number of iterations of the tool calls" )
    research_topic: str                                                      = Field ( default = "", description = "The topic to search" )
    compressed_research: str                                                 = Field ( default = "", description = "The compressed search" )
    raw_notes: Annotated [ List [ str ], operator.add ]                      = Field ( default = [], description = "The raw research notes" )


class ResearcherOutputState ( BaseModel ):
    """
    Output state for the research agent containing final research results.

    This represents the final output of the research process with compressed
    research findings and all raw notes from the research process.
    """
    researcher_messages: Annotated [ Sequence [ AnyMessage ], add_messages ] = Field ( default = [], description = "Messages to be sent to the user" )
    compressed_research: str                                                 = Field ( default = "", description = "The compressed search" )
    raw_notes: Annotated [ List [ str ], operator.add ]                      = Field ( default = [], description = "The raw research notes" )



# ===== STRUCTURED OUTPUT SCHEMAS =====
class ResearchQuestion ( BaseModel ):
    """Schema for research brief generation."""
    research_brief: str = Field ( description = "A research question that will be used to guide the research" )


class Summary ( BaseModel ):
    """Schema for webpage content summarization."""
    summary: str      = Field ( description = "Concise summary of the webpage content" )
    key_excerpts: str = Field ( description = "Important quotes and excerpts from the content" )
