from langchain.chat_models import init_chat_model
from langgraph.constants import START, END
from langgraph.graph import MessagesState, StateGraph

from src.deep_search_langgraph.common.common import LLM_MODEL_NAME
from src.deep_search_langgraph.common.prompts import writer_prompt

NODE_WRITER: str = "writer"


class Writer:

    def __init__ ( self ):
        pass
    

    def writer ( self, state: MessagesState ):

        return { "messages": [ init_chat_model ( model = LLM_MODEL_NAME ).invoke ( [ writer_prompt ] + state [ "messages" ] ) ] }


    def build_graph ( self ):
        builder = StateGraph ( MessagesState )
        builder.add_node ( NODE_WRITER, self.writer )

        builder.add_edge ( START, NODE_WRITER )
        builder.add_edge ( NODE_WRITER, END )

        return builder.compile ()


graph = Writer ().build_graph ()