from langgraph.constants import START, END
from langgraph.graph import MessagesState, StateGraph
from src.deep_search_langgraph.common.common import get_today_str, get_llm
from src.deep_search_langgraph.common.prompts import searcher_prompt

NODE_SEARCHER: str = "searcher"


class Searcher:

    def __init__ ( self ):
        pass


    def searcher ( self, state: MessagesState ):

        return { "messages": [ get_llm ().invoke ( [ searcher_prompt ] + state [ "messages" ] ) ] }


    def build_graph ( self ):
        builder = StateGraph ( MessagesState )
        builder.add_node ( NODE_SEARCHER, self.searcher )

        builder.add_edge ( START, NODE_SEARCHER )
        builder.add_edge ( NODE_SEARCHER, END )

        return builder.compile ()


graph = Searcher ().build_graph ()    