class MemoryRouter:

    def route(self, user_input: str):

        text = user_input.lower()

        # CREATE
        if text.startswith("my "):

            if "favorite color is" in text:
                return {
                    "intent": "memory",
                    "action": "create",
                    "entities": {
                        "category": "personal",
                        "key": "favorite_color",
                        "value": user_input.split("is", 1)[1].strip()
                    },
                    "confidence": 1.0
                }

            if "birthday is" in text:
                return {
                    "intent": "memory",
                    "action": "create",
                    "entities": {
                        "category": "personal",
                        "key": "birthday",
                        "value": user_input.split("is", 1)[1].strip()
                    },
                    "confidence": 1.0
                }

            if "name is" in text:
                return {
                    "intent": "memory",
                    "action": "create",
                    "entities": {
                        "category": "personal",
                        "key": "name",
                        "value": user_input.split("is", 1)[1].strip()
                    },
                    "confidence": 1.0
                }

        # READ
        if "favorite color" in text:
            return {
                "intent": "memory",
                "action": "read",
                "entities": {
                    "key": "favorite_color"
                },
                "confidence": 1.0
            }

        if "my birthday" in text:
            return {
                "intent": "memory",
                "action": "read",
                "entities": {
                    "key": "birthday"
                },
                "confidence": 1.0
            }

        if "my name" in text:
            return {
                "intent": "memory",
                "action": "read",
                "entities": {
                    "key": "name"
                },
                "confidence": 1.0
            }

        return None