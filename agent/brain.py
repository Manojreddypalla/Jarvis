# agent/brain.py

from config import Config

from llm.ollama import chat_ollama
from llm.openai import chat_openai

from tools.shell import run_command


# -----------------------
# Call LLM
# -----------------------

def call_llm(messages):

    if Config.llm_type == "ollama":

        return chat_ollama(
            messages,
            Config.model
        )


    if Config.llm_type == "openai":

        return chat_openai(
            messages,
            Config.api_key,
            Config.model
        )


    return "No LLM"


# -----------------------
# Tool Handler
# -----------------------

def handle_tool(result, user_input):

    if "run_command" in result.lower():

        output = run_command(user_input)

        observe = {
            "tool": "run_command",
            "input": user_input,
            "output": output
        }

        return observe


    return None


# -----------------------
# Brain
# -----------------------

def think_and_act(messages, user_input):

    result = call_llm(messages)

    observe = handle_tool(result, user_input)

    return result, observe
