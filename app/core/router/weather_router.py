class WeatherRouter:

    def route(self, user_input: str):

        text = user_input.lower()

        if "weather" not in text:
            return None

        location = None

        if " in " in text:
            location = user_input.split(" in ", 1)[1].strip()

        return {
            "intent": "weather",
            "action": "read",
            "entities": {
                "location": location
            },
            "confidence": 1.0
        }