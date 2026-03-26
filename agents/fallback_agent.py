from pipeline.llm import get_llm


class FallbackAgent:

    def __init__(self):
        self.llm = get_llm()

    def handle(self, user_query: str) -> str:

        system_prompt = """
        You are OmniBank Assistant.

        Rules:
        - Do NOT access account data.
        - Do NOT assume balances.
        - Do NOT perform transactions.
        - Only answer general informational questions.
        - Keep answers concise and professional.
        """

        response = self.llm.invoke(
            system_prompt + "\nUser: " + user_query
        )

        return response.content