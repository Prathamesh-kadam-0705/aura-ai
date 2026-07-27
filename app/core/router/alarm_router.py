import re


class AlarmRouter:

    def route(self, user_input: str):

        text = user_input.lower()

        if "alarm" not in text:
            return None

        time_match = re.search(
            r'(\d{1,2}(:\d{2})?\s?(am|pm))',
            user_input,
            re.IGNORECASE
        )

        time = time_match.group(1) if time_match else None

        return {
            "intent": "alarm",
            "action": "create",
            "entities": {
                "time": time
            },
            "confidence": 1.0
        }