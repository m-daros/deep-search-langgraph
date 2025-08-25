import ast
from typing import Literal

from langchain_core.language_models import BaseChatModel
from langgraph.constants import START, END
from langgraph.graph import MessagesState, StateGraph

from src.deep_search_langgraph.common.common import get_today_str, get_llm
from src.deep_search_langgraph.common.prompts import clarify_with_user, transform_messages_into_research_topic
from src.deep_search_langgraph.planner.planner_state import PlannerAgentState

NODE_PLAN_SEARCH: str       = "plan_searches"
NODE_CLARIFY_WITH_USER: str = "clarify_with_user"


class Planner:

    def __init__ ( self ):
        pass


    def plan_searches ( self, state: PlannerAgentState ):
        # Proceed with planning
        
        message = transform_messages_into_research_topic.format ( messages = state.messages, date = get_today_str () )
        
        return { "messages": [ get_llm ().invoke ( [ message ] ) ] }


    def clarify_with_user ( self , state: PlannerAgentState ):

        message = clarify_with_user.format ( messages = state.messages, date = get_today_str () )
        clarification = get_llm ().with_structured_output ( PlannerAgentState ).invoke ( message )
        
        if clarification.need_clarification:
            # Add the question as an AI message
            from langchain_core.messages import AIMessage
            question_message = AIMessage ( content = clarification.question )

            return PlannerAgentState ( messages = state.messages + [ question_message ],
                                       need_clarification = clarification.need_clarification,
                                       question = clarification.question,
                                       verification = None )
        else:
            # Add verification message and proceed
            from langchain_core.messages import AIMessage
            verification_message = AIMessage ( content = clarification.verification )

            return PlannerAgentState ( messages = state.messages + [ verification_message ],
                                       need_clarification = clarification.need_clarification,
                                       question = None,
                                       verification = clarification.verification )


    def need_clarification ( self, state: PlannerAgentState ) -> Literal [ "__end__", "plan_searches" ]:
#    def need_clarification ( self, state: PlannerAgentState ) -> Literal [ "clarify_with_user", "plan_searches" ]:

        if state.need_clarification:
            return END
#            return "clarify_with_user"

        else:
            return "plan_searches"




    def build_graph ( self ):

        builder = StateGraph ( PlannerAgentState )
        builder.add_node ( NODE_CLARIFY_WITH_USER, self.clarify_with_user )
        builder.add_node ( NODE_PLAN_SEARCH, self.plan_searches )

        builder.add_edge ( START, NODE_CLARIFY_WITH_USER )
        builder.add_conditional_edges ( NODE_CLARIFY_WITH_USER, self.need_clarification )
        builder.add_edge ( NODE_PLAN_SEARCH, END )

        return builder.compile ()

planner = Planner ()
graph = planner.build_graph ()

# TODO La logicaad oggetti non sembra facilitare l'uso dei metodi (nodi) da parte del grafo principale
def plan_searches ( state: PlannerAgentState ):
    return planner.plan_searches ( state )