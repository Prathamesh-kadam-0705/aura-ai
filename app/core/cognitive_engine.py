from app.core.router.router_manager import RouterManager
from app.llm.local_llm import LocalLLM
from app.models.request import Request
from app.core.conversation_state import ConversationState



class CognitiveEngine:

    def __init__(self):
        self.router = RouterManager()
        self.llm = LocalLLM()

    def process(self, user_input):

        # Check previous unfinished conversation
        if ConversationState.pending:

            pending = ConversationState.pending

            entities = self.router.entity_router.route(
                pending["intent"],
                pending["action"],
                user_input
            )

            return Request(
                intent=pending["intent"],
                action=pending["action"],
                entities=entities,
                confidence=1.0
            )


        # Normal flow
        result = self.router.process(user_input)

        if result:
            print("✅ Router:", result)
            return Request(**result)


        result = self.llm.understand(user_input)

        print("🧠 LLM:", result)

        return Request(**result)