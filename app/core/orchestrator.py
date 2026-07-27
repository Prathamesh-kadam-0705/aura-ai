from app.core.decision_engine import DecisionEngine
from app.core.response_generator import ResponseGenerator
from app.core.response_handler import ResponseHandler


class Orchestrator:

    def __init__(self):
        self.decision_engine = DecisionEngine()
        self.response_handler = ResponseHandler()

    def process(self, request):

        # Conversation Layer
        if request.intent == "conversation":

            if request.action == "greeting":

                return ResponseGenerator.success(
                    answer="Hello Prathamesh. I am AURA. How can I help you today?",
                    message="Greeting generated.",
                    payload={
                        "topic": "greeting"
                    }
                )

        tool = self.decision_engine.decide(request)

        if tool is None:
            return ResponseGenerator.error(
                f"No tool found for '{request.intent}'."
            )

        action = getattr(tool, request.action, None)

        if action is None:
            return ResponseGenerator.error(
                f"Action '{request.action}' not supported."
            )

        # Execute the tool
        result = action(request)

        # Let ResponseHandler build the final API response
        return self.response_handler.build(request, result)