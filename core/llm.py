import google.generativeai as genai
from langchain_ollama import OllamaLLM

from core.config import Config


class LLMManager:

    def __init__(self, choice: str):

        self.use_ollama = False
        self.use_gemini = False


        if choice == "1":

            self.llm = OllamaLLM(
                model=Config.OLLAMA_MODEL,
                base_url=Config.OLLAMA_URL
            )

            self.use_ollama = True


        elif choice == "2":

            if not Config.GEMINI_KEY:
                raise ValueError("GEMINI key missing")

            genai.configure(api_key=Config.GEMINI_KEY)

            self.llm = genai.GenerativeModel("gemini-2.5-flash")

            self.use_gemini = True


        else:
            raise ValueError("Invalid LLM choice")


    def call(self, prompt: str) -> str:

        try:

            if self.use_ollama:
                return str(self.llm.invoke(prompt))

            if self.use_gemini:
                return self.llm.generate_content(prompt).text.strip()

        except Exception as e:

            print("❌ LLM Error:", e)
            return ""
