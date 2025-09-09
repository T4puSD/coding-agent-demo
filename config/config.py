import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
        if not self.GEMINI_API_KEY or self.GEMINI_API_KEY == "":
            raise ValueError("Please provde a valid GEMINI_API_KEY as env value")
        self.FILE_CONTENT_MAX_READ_SIZE = int(os.environ.get("FILE_CONTENT_MAX_READ_SIZE", 10000))
        self.AI_AGENT_WORKING_DIRECTORY = os.environ.get("AI_AGENT_WORKING_DIRECTORY", "./calculator")

config = Config()