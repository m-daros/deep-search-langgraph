from langgraph.constants import START, END
from langgraph.graph import StateGraph, MessagesState

from src.deep_search_langgraph.planner.planner import graph as planner_graph
from src.deep_search_langgraph.searcher.searcher import graph as searcher_graph
from src.deep_search_langgraph.writer.writer import graph as writer_graph

NODE_PLAN_SUBGRAPH: str   = "plan_subgraph"
NODE_SEARCH_SUBGRAPH: str = "search_subgraph"
NODE_WRITE_SUBGRAPH: str  = "write_subgraph"


builder = StateGraph ( MessagesState )
builder.add_node ( NODE_PLAN_SUBGRAPH, planner_graph )
builder.add_node ( NODE_SEARCH_SUBGRAPH, searcher_graph )
builder.add_node ( NODE_WRITE_SUBGRAPH, writer_graph )

builder.add_edge ( START, NODE_PLAN_SUBGRAPH )
builder.add_edge ( NODE_PLAN_SUBGRAPH, NODE_SEARCH_SUBGRAPH )
builder.add_edge ( NODE_SEARCH_SUBGRAPH, NODE_WRITE_SUBGRAPH )
builder.add_edge ( NODE_WRITE_SUBGRAPH, END )

graph = builder.compile ()