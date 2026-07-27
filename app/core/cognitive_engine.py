from app.core.router.router_manager import RouterManager
from app.llm.local_llm import LocalLLM
from app.models.request import Request


class CognitiveEngine:

    def __init__(self):
        self.router = RouterManager()
        self.llm = LocalLLM()

    def process(self, user_input):

        result = self.router.process(user_input)

        if result:
            print("✅ Router:", result)
            return Request(**result)

        result = self.llm.understand(user_input)

        print("🧠 LLM:", result)
        print("RESULT TYPE:", type(result))
        print("RESULT:", result)
        return Request(**result)