# app/runner.py

import json

from config import Config
from agent.prompt import SYSTEM_PROMPT
from agent.brain import think_and_act
from llm.selector import select_llm


def run():

    print("🤖 CLI Agent V2\n")


    ok = select_llm()

    if not ok:
        print("Invalid LLM")
        return


    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]


    print("\n✅ Ready (type exit)\n")


    while True:

        user = input("You: ")

        if user == "exit":
            break


        messages.append({
            "role": "user",
            "content": user
        })


        result, observe = think_and_act(messages, user)


        print("\n🤖 Agent:", result, "\n")


        messages.append({
            "role": "assistant",
            "content": result
        })


        if observe:

            messages.append({
                "role": "developer",
                "content": json.dumps(observe)
            })
