from datetime import datetime


LLM_MODEL_NAME: str = "google_genai:gemini-2.0-flash"

def get_today_str () -> str:
    """Get current date in a human-readable format."""
    return datetime.now ().strftime ( "%a %b %-d, %Y" )
