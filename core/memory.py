from core.prompt import SYSTEM_PROMPT


class Memory:

    def __init__(self):

        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]


    def add_user(self, text: str):

        self.messages.append({
            "role": "user",
            "content": text
        })


    def add_ai(self, text: str):

        self.messages.append({
            "role": "assistant",
            "content": text
        })


    def add_system(self, text: str):

        self.messages.append({
            "role": "system",
            "content": text
        })


    def build_prompt(self):

        return "\n".join(
            f"{m['role'].upper()}: {m['content']}"
            for m in self.messages
        )
