from typing import Literal

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import interrupt

from src.deep_search_langgraph.common.common import get_today_str, LLM_MODEL_NAME
from src.deep_search_langgraph.common.prompts import clarify_with_user, transform_messages_into_research_topic
from src.deep_search_langgraph.planner.planner_state import PlannerAgentState, AskHuman



NODE_PLAN_SEARCH: str       = "plan_searches"
NODE_CLARIFY_WITH_USER: str = "clarify_with_user"
NODE_ASK_HUMAN: str         = "ask_human"


class Planner:

    def __init__ ( self ):
        pass


    def plan_searches ( self, state: PlannerAgentState ):
        # Proceed with planning
        
        message = transform_messages_into_research_topic.format ( messages = state.messages, date = get_today_str () )
        
        return { "messages": [ init_chat_model ( model = LLM_MODEL_NAME ).invoke ( input = [ message ] ) ] }


    def clarify_with_user ( self , state: PlannerAgentState ):

        message = clarify_with_user.format ( messages = state.messages, date = get_today_str () )
        clarification = init_chat_model ( model = LLM_MODEL_NAME ).bind_tools ( tools = [ AskHuman ] ).with_structured_output ( PlannerAgentState ).invoke ( input = [ message ] )
        
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


    def need_clarification ( self, state: PlannerAgentState ) -> Literal [ "ask_human", "plan_searches" ]:

        if state.need_clarification:
            return "ask_human"
        else:
            return "plan_searches"

    def ask_human ( self, state: PlannerAgentState ):

        user_answer = interrupt ( state.question )

        return PlannerAgentState ( messages = state.messages + [ HumanMessage ( content = user_answer ) ],
                                   need_clarification = state.need_clarification,
                                   question = state.question,
                                   verification = state.verification )


    def build_graph ( self ):

        builder = StateGraph ( PlannerAgentState )
        builder.add_node ( NODE_CLARIFY_WITH_USER, self.clarify_with_user )
        builder.add_node ( NODE_ASK_HUMAN, self.ask_human )
        builder.add_node ( NODE_PLAN_SEARCH, self.plan_searches )

        builder.add_edge ( START, NODE_CLARIFY_WITH_USER )
        builder.add_edge ( NODE_ASK_HUMAN, NODE_CLARIFY_WITH_USER )
        builder.add_conditional_edges ( NODE_CLARIFY_WITH_USER, self.need_clarification )
        builder.add_edge ( NODE_PLAN_SEARCH, END )

        return builder.compile ()


planner = Planner ()
graph = planner.build_graph ()