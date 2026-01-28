# core/prompt.py


def build_prompt(messages):

    text = ""

    for msg in messages:

        role = msg["role"]
        content = msg["content"]

        text += f"{role.upper()}: {content}\n"

    return text
