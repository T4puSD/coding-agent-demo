from config.config import config

def get_api_key():
    """Get the Gemini API key from configuration."""
    return config.GEMINI_API_KEY

def get_working_directory():
    """Get the AI agent working directory from configuration."""
    return config.AI_AGENT_WORKING_DIRECTORY
