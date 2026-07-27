class TodoRouter:

    def route(self, user_input: str):

        text = user_input.lower()

        if text.startswith("add todo"):

            return {
                "intent": "todo",
                "action": "create",
                "entities": {
                    "task": user_input.replace("Add Todo", "").replace("add todo", "").strip()
                },
                "confidence": 1.0
            }

        if "todo list" in text:

            return {
                "intent": "todo",
                "action": "list",
                "entities": {},
                "confidence": 1.0
            }

        return None