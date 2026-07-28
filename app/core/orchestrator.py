from app.core.decision_engine import DecisionEngine
from app.core.response_generator import ResponseGenerator
from app.core.response_handler import ResponseHandler
from app.core.conversation_state import ConversationState
from app.core.request_validator import RequestValidator
from app.llm.local_llm import LocalLLM


class Orchestrator:

    def __init__(self):
        self.decision_engine = DecisionEngine()
        self.response_handler = ResponseHandler()
        self.llm = LocalLLM()


    def process(self, request):

        # -----------------------------
        # Conversation Layer
        # -----------------------------
        if request.intent == "conversation":

            if request.action == "greeting":

                return ResponseGenerator.success(
                    answer="Hello Prathamesh. I am AURA. How can I help you today?",
                    message="Greeting generated.",
                    payload={
                        "topic": "greeting"
                    }
                )


        # -----------------------------
        # Validate Required Entities
        # -----------------------------
        missing = RequestValidator.validate(request)


        if missing:

            ConversationState.pending = {

                "intent": request.intent,
                "action": request.action,
                "missing": missing

            }


            # Generate AI question
            question = self.llm.generate_missing_question(
                request,
                missing
            )


            return ResponseGenerator.success(

                answer=question,

                message="Waiting for user input.",

                payload={
                    "need_input": True,
                    "missing": missing
                }

            )


        # -----------------------------
        # Decision Layer
        # -----------------------------
        tool = self.decision_engine.decide(request)


        if tool is None:

            return ResponseGenerator.error(
                f"No tool found for '{request.intent}'."
            )


        action = getattr(
            tool,
            request.action,
            None
        )


        if action is None:

            return ResponseGenerator.error(
                f"Action '{request.action}' not supported."
            )


        # -----------------------------
        # Execute Tool
        # -----------------------------
        result = action(request)


        # Clear pending after success
        ConversationState.pending = None


        # -----------------------------
        # Build Response
        # -----------------------------
        return self.response_handler.build(
            request,
            result
        )