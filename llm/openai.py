# llm/openai.py

from openai import OpenAI


def chat_openai(messages, api_key, model):

    client = OpenAI(api_key=api_key)

    res = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return res.choices[0].message.content
