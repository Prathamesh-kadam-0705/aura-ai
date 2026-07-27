class DeviceRouter:

    def route(self, user_input: str):

        text = user_input.lower()

        if text.startswith("open "):

            return {
                "intent": "device",
                "action": "open",
                "entities": {
                    "app": user_input[5:].strip()
                },
                "confidence": 1.0
            }

        if text.startswith("close "):

            return {
                "intent": "device",
                "action": "close",
                "entities": {
                    "app": user_input[6:].strip()
                },
                "confidence": 1.0
            }

        return None