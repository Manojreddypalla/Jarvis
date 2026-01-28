# llm_factory.py
import os
import ollama
from openai import OpenAI
import google.generativeai as genai

class LLMFactory:
    def __init__(self, config):
        self.config = config
        self.provider = config['provider']
        
    def call(self, messages):
        if self.provider == "ollama":
            resp = ollama.chat(model=self.config['model'], messages=messages)
            return {"role": "assistant", "content": resp['message']['content']}
        
        elif self.provider == "openai":
            client = OpenAI(api_key=self.config['key'])
            resp = client.chat.completions.create(model=self.config['model'], messages=messages)
            return resp.choices[0].message
            
        elif self.provider == "gemini":
            genai.configure(api_key=self.config['key'])
            model = genai.GenerativeModel(self.config['model'])
            # Gemini expects simple strings or specific history; we send the last user message for now
            resp = model.generate_content(messages[-1]['content'])
            return {"role": "assistant", "content": resp.text}




            #This file handles the messy API calls. It makes main.py look clean because main.py just calls one function.