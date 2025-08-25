from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models import BaseChatModel

llm_model: str = "gemini-2.0-flash"

def get_today_str () -> str:
    """Get current date in a human-readable format."""
    return datetime.now ().strftime ( "%a %b %-d, %Y" )


def get_llm () -> BaseChatModel:
    return ChatGoogleGenerativeAI ( model = llm_model )