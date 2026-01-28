# llm/selector.py

from config import Config


def select_llm():

    print("\nSelect LLM:\n")
    print("1. Local (Ollama)")
    print("2. OpenAI (Cloud)")

    choice = input("Enter choice: ")


    if choice == "1":

        model = input("Enter Ollama model: ")

        Config.llm_type = "ollama"
        Config.model = model

        return True


    if choice == "2":

        key = input("Enter OpenAI API Key (temp): ")

        Config.llm_type = "openai"
        Config.api_key = key
        Config.model = "gpt-4o-mini"

        return True


    return False
