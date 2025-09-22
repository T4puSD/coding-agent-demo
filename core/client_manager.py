from google import genai
from core.config_manager import get_api_key

def create_client():
    """Create and return a Gemini API client."""
    api_key = get_api_key()
    return genai.Client(api_key=api_key)
