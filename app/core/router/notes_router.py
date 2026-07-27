class NotesRouter:

    def route(self, user_input: str):

        text = user_input.lower()

        if text.startswith("create note"):

            return {
                "intent": "notes",
                "action": "create",
                "entities": {
                    "content": user_input
                },
                "confidence": 1.0
            }

        if text.startswith("show notes"):

            return {
                "intent": "notes",
                "action": "list",
                "entities": {},
                "confidence": 1.0
            }

        return None