from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage

from src.deep_search_langgraph.common.model.deep_search_state import DeepSearchState
from src.deep_search_langgraph.planner.planner import graph as planner_graph
from src.deep_search_langgraph.searcher.searcher import graph as searcher_graph
from src.deep_search_langgraph.writer.writer import graph as writer_graph

NODE_PLAN_SUBGRAPH: str   = "plan_subgraph"
NODE_SEARCH_SUBGRAPH: str = "search_subgraph"
NODE_WRITE_SUBGRAPH: str  = "write_subgraph"

def call_planner_subgraph(state: DeepSearchState):
    """Wrapper function to properly map state for the planner subgraph."""
    from src.deep_search_langgraph.planner.planner_state import PlannerAgentState
    
    # Create the planner input state
    planner_input = PlannerAgentState(
        messages=state.messages,
        need_clarification=False,
        question=None,
        verification=None,
        research_brief=None
    )
    
    # Call the planner subgraph
    planner_result = planner_graph.invoke(planner_input)
    
    # Map the result back to DeepSearchState
    return {
        "messages": planner_result.get("messages", state.messages),
        "research_brief": planner_result.get("research_brief", "")
    }

def call_searcher_subgraph(state: DeepSearchState):
    """Wrapper function to properly map state for the searcher subgraph."""
    from src.deep_search_langgraph.searcher.searcher_state import ResearcherState
    
    # Create a human message with the research brief to start the research
    research_message = HumanMessage(content=state.research_brief) if state.research_brief else None
    
    searcher_input = ResearcherState(
        researcher_messages=[research_message] if research_message else [],
        research_topic=state.research_brief or "",
        tool_call_iterations=0,
        compressed_research="",
        raw_notes=[]
    )
    
    # Call the searcher subgraph
    searcher_result = searcher_graph.invoke(searcher_input)
    
    # Map the result back to DeepSearchState
    return {
        "research_result": searcher_result.get("compressed_research", ""),
        "messages": state.messages  # Keep original messages
    }

def call_writer_subgraph(state: DeepSearchState):
    """Wrapper function to properly map state for the writer subgraph."""
    from langgraph.graph import MessagesState
    
    # Create the writer input state
    writer_input = MessagesState(
        messages=state.messages,
        research_result=state.research_result
    )
    
    # Call the writer subgraph
    writer_result = writer_graph.invoke(writer_input)
    
    # Map the result back to DeepSearchState
    return {
        "messages": writer_result.get("messages", state.messages)
    }

builder = StateGraph ( DeepSearchState )
builder.add_node ( NODE_PLAN_SUBGRAPH, call_planner_subgraph )
builder.add_node ( NODE_SEARCH_SUBGRAPH, call_searcher_subgraph )
builder.add_node ( NODE_WRITE_SUBGRAPH, call_writer_subgraph )

builder.add_edge ( START, NODE_PLAN_SUBGRAPH )
builder.add_edge ( NODE_PLAN_SUBGRAPH, NODE_SEARCH_SUBGRAPH )
builder.add_edge ( NODE_SEARCH_SUBGRAPH, NODE_WRITE_SUBGRAPH )
builder.add_edge ( NODE_WRITE_SUBGRAPH, END )

graph = builder.compile ()