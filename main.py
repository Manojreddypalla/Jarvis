import os
import json
from dotenv import load_dotenv
from openai import OpenAI


# -----------------------
# Load API Key
# -----------------------

load_dotenv()

client = OpenAI()


# -----------------------
# TOOL: Run Command
# -----------------------

def run_command(cmd):

    result = os.system(cmd)

    return result


# -----------------------
# Available Tools
# -----------------------

available_tools = {
    "run_command": run_command
}


# -----------------------
# System Prompt (V2 Agent)
# -----------------------

SYSTEM_PROMPT = """
You are a CLI AI agent.

You can think step by step.

You have this tool:

run_command(command)

Use it when needed.

Follow this loop:

THINK -> PLAN -> ACT -> OBSERVE -> ANSWER

When you want to use a tool,
explicitly say: use run_command
"""


# -----------------------
# Main
# -----------------------

def main():

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]


    print("🤖 CLI Agent V2 Started\n")


    while True:

        user = input("You: ")

        if user == "exit":
            break


        messages.append({
            "role": "user",
            "content": user
        })


        # -----------------------
        # Call LLM
        # -----------------------

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )


        result = response.choices[0].message.content


        print("\n🤖 Agent:", result, "\n")


        messages.append({
            "role": "assistant",
            "content": result
        })


        # -----------------------
        # Tool Detection
        # -----------------------

        if "run_command" in result.lower():

            cmd = user

            print("🔧 Running:", cmd)


            output = available_tools["run_command"](cmd)


            print("📡 Output:", output)


            # -----------------------
            # Observe Step
            # -----------------------

            observe = {
                "step": "observe",
                "tool": "run_command",
                "input": cmd,
                "output": output
            }


            messages.append({
                "role": "developer",
                "content": json.dumps(observe)
            })


# -----------------------
# Run
# -----------------------

main()
