# main.py

import json
import requests


# -----------------------
# Ollama Client
# -----------------------
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3"   # or mistral, phi, etc


def call_local_llm(messages):
    """
    Send messages to Ollama
    """

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }

    res = requests.post(OLLAMA_URL, json=payload)

    if res.status_code == 200:
        return res.json()["message"]["content"]

    return "LLM Error"


# -----------------------
# Tools (Prototype)
# -----------------------

def analyze_repo(repo_url):
    return f"[Prototype] Repo analysis started for: {repo_url}"


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()[:2000]
    except:
        return "Cannot read file"


# Tool Registry
available_tools = {
    "analyze_repo": analyze_repo,
    "read_file": read_file
}


# -----------------------
# System Prompt
# -----------------------

SYSTEM_PROMPT = """
You are a personal AI agent.

You can use tools:

- analyze_repo(repo_url)
- read_file(path)

If user asks about a repository,
use analyze_repo.

If user asks to read a file,
use read_file.

Follow steps:
start -> plan -> tool -> observe -> output
"""


# -----------------------
# Main Loop
# -----------------------

def main():

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    print("🤖 Local AI Assistant Started (Type 'exit' to quit)\n")

    while True:

        user = input("You: ")

        if user.lower() == "exit":
            break

        messages.append({
            "role": "user",
            "content": user
        })

        # Call Local LLM
        result = call_local_llm(messages)

        print("\n🤖 Agent:", result, "\n")

        messages.append({
            "role": "assistant",
            "content": result
        })

        # -----------------------
        # Tool Detection
        # -----------------------

        # Repo Tool
        if "analyze_repo" in result:

            repo = user.split()[-1]

            print("🔧 Tool: analyze_repo ->", repo)

            output = available_tools["analyze_repo"](repo)

            print("📡 Result:", output)

            observe = {
                "step": "observe",
                "tool": "analyze_repo",
                "input": repo,
                "output": output
            }

            messages.append({
                "role": "developer",
                "content": json.dumps(observe)
            })


        # File Tool
        elif "read_file" in result:

            path = user.split()[-1]

            print("🔧 Tool: read_file ->", path)

            output = available_tools["read_file"](path)

            print("📡 Result:\n", output)

            observe = {
                "step": "observe",
                "tool": "read_file",
                "input": path,
                "output": output[:1500]
            }

            messages.append({
                "role": "developer",
                "content": json.dumps(observe)
            })


# -----------------------
# Run
# -----------------------

if __name__ == "__main__":
    main()
