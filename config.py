# config.py

import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # "ollama" or "gemini"
    llm_type = None

    # Ollama model
    ollama_model = "llama3"

    # Gemini
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    gemini_model = "gemini-2.5-flash"
