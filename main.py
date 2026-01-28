# main.py

import os
import json
from dotenv import load_dotenv

import google.generativeai as genai
from langchain_ollama import OllamaLLM

from tools.registry import TOOLS


# ------------------------
# Load Env
# ------------------------

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY")


# ------------------------
# Choose LLM
# ------------------------

print("""
Select LLM:

1️⃣ Ollama (llama3 - Local)
2️⃣ Gemini (2.5 Flash - Cloud)
""")

choice = input("Enter choice (1/2): ").strip()


# ------------------------
# Setup Model
# ------------------------

USE_OLLAMA = False
USE_GEMINI = False


if choice == "1":

    print("✅ Using Ollama (llama3)\n")

    llm = OllamaLLM(
        model="llama3",
        base_url="http://localhost:11434"
    )

    USE_OLLAMA = True


elif choice == "2":

    if not GEMINI_KEY:
        raise ValueError("❌ GEMINI_API_KEY not found in .env")

    print("✅ Using Gemini (2.5 Flash)\n")

    genai.configure(api_key=GEMINI_KEY)

    gemini_model = genai.GenerativeModel("gemini-2.5-flash")

    USE_GEMINI = True


else:
    raise ValueError("❌ Invalid choice. Enter 1 or 2.")


# ------------------------
# System Prompt
# ------------------------

SYSTEM_PROMPT = """
You are Jarvis, a personal AI assistant.

Available tools:

1. run_command(cmd)
   → Run system commands.

2. index_pdf(file_path)
   → Learn from PDF.

3. search_rag(query)
   → Answer from learned docs.


4. ingest_data_folder()
   → Scan data folder and ingest all PDF, DOCX, MD files.

Use ingest_data_folder when user says:
- ingest files
- import documents
- learn new files
- scan data folder

Rules:

- For system tasks → run_command
- For learning PDFs → index_pdf
- For document questions → search_rag

If tool needed, reply ONLY in JSON:

{
  "tool": "<name>",
  "input": "<string>"
}

Otherwise reply normally.
"""


# ------------------------
# Memory
# ------------------------

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]


# ------------------------
# LLM Call Wrapper
# ------------------------

def call_llm(prompt: str) -> str:

    # Ollama
    if USE_OLLAMA:
        return llm.invoke(prompt)

    # Gemini
    if USE_GEMINI:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()


# ------------------------
# Main Loop
# ------------------------

print("🤖 Jarvis Agent Started\n")

while True:

    user = input("You: ")

    if user.lower() in ["exit", "quit"]:
        break


    messages.append({
        "role": "user",
        "content": user
    })


    # Build Prompt
    prompt = ""

    for m in messages:
        prompt += f"{m['role'].upper()}: {m['content']}\n"


    # Call LLM
    raw = call_llm(prompt)


    # Try Tool Call
    try:
        data = json.loads(raw)

        tool = data["tool"]
        inp = data["input"]


        if tool in TOOLS:

            print(f"🛠️ Using: {tool}")

            result = TOOLS[tool](inp)

            print("📡", result)


            messages.append({
                "role": "assistant",
                "content": raw
            })

            messages.append({
                "role": "user",
                "content": f"Tool result: {result}"
            })

            continue

    except:
        pass


    # Normal Answer
    print("AI:", raw, "\n")


    messages.append({
        "role": "assistant",
        "content": raw
    })
