from core.llm import LLMManager
from core.memory import Memory
from core.agent import Agent

from tools.registry import TOOLS


def run():

    print("""
Select LLM:

1) Ollama
2) Gemini
""")

    choice = input("Enter choice: ").strip()

    llm = LLMManager(choice)

    memory = Memory()

    agent = Agent(llm, memory, TOOLS)


    print("🤖 Jarvis Started\n")


    while True:

        user = input("You: ").strip()

        if user.lower() in ["exit", "quit"]:
            print("👋 Bye!")
            break

        if not user:
            continue

        agent.step(user)
