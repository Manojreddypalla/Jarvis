from core.parser import parse_json


class Agent:

    def __init__(self, llm, memory, tools):

        self.llm = llm
        self.memory = memory
        self.tools = tools


    def step(self, user_input: str):

        self.memory.add_user(user_input)

        prompt = self.memory.build_prompt()

        raw = self.llm.call(prompt)

        if not raw:
            print("⚠️ Empty response")
            return


        # Try tool
        try:

            data = parse_json(raw)

            tool = data.get("tool")
            inp = data.get("input", "")


            if tool in self.tools:

                print(f"\nAI: Running {tool}...\n")

                result = self.tools[tool](inp)


                # Print output
                if isinstance(result, str):

                    for line in result.split("\n"):
                        if line.strip():
                            print("AI:", line)

                else:
                    print("AI:", result)


                self.memory.add_ai(raw)
                self.memory.add_system(f"Tool result:\n{result}")


                # Final response
                final = self.llm.call(
                    self.memory.build_prompt()
                )

                print("AI:", final, "\n")

                self.memory.add_ai(final)

                return


        except:
            pass


        # Normal reply
        print("AI:", raw, "\n")

        self.memory.add_ai(raw)
