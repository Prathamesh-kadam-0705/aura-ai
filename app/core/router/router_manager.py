from app.core.router.intent_router import IntentRouter
from app.core.router.action_router import ActionRouter
from app.core.router.entity_router import EntityRouter


class RouterManager:

    def __init__(self):
        self.intent_router = IntentRouter()
        self.action_router = ActionRouter()
        self.entity_router = EntityRouter()

    def process(self, user_input):

        result = self.intent_router.route(user_input)

        if result is None:
            return None

        entities = self.entity_router.route(
            result["intent"],
            result["action"],
            user_input
        )

        result["entities"] = entities

        return result