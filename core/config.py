import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    GEMINI_KEY = os.getenv("GEMINI_API_KEY")

    OLLAMA_URL = "http://localhost:11434"
    OLLAMA_MODEL = "llama3"
