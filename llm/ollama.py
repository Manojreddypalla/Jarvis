# llm/ollama.py

import requests


def chat_ollama(messages, model):

    url = "http://localhost:11434/api/chat"

    payload = {
        "model": model,
        "messages": messages,
        "stream": False
    }

    r = requests.post(url, json=payload)

    if r.status_code == 200:
        return r.json()["message"]["content"]

    return "Ollama Error"
