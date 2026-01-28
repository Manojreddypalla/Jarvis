# main.py

from config import Config

from llm.selector import select_llm
from llm.ollama import chat_ollama
from llm.openai import chat_openai

from core.prompt import build_prompt


# -----------------------
# Main
# -----------------------

def main():

    print("🤖 Personal AI Assistant - V1\n")


    ok = select_llm()

    if not ok:
        print("Invalid LLM")
        return


    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        }
    ]


    print("\n✅ LLM Ready")
    print("Type 'exit' to quit\n")


    while True:

        user = input("You: ")

        if user == "exit":
            break


        messages.append({
            "role": "user",
            "content": user
        })


        prompt = build_prompt(messages)


        # -----------------------
        # Route LLM
        # -----------------------

        if Config.llm_type == "ollama":

            answer = chat_ollama(
                messages,
                Config.model
            )


        elif Config.llm_type == "openai":

            answer = chat_openai(
                messages,
                Config.api_key,
                Config.model
            )


        else:
            answer = "No LLM"


        print("\n🤖 Agent:", answer, "\n")


        messages.append({
            "role": "assistant",
            "content": answer
        })


# -----------------------
# Run
# -----------------------

main()
