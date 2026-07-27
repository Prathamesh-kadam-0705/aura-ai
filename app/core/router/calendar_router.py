import re


class CalendarRouter:

    def route(self, user_input: str):

        text = user_input.lower()

        if not any(word in text for word in [
            "meeting",
            "schedule",
            "appointment",
            "calendar"
        ]):
            return None

        date = None
        time = None

        if "tomorrow" in text:
            date = "tomorrow"
        elif "today" in text:
            date = "today"

        time_match = re.search(
            r'(\d{1,2}(:\d{2})?\s?(am|pm))',
            user_input,
            re.IGNORECASE
        )

        if time_match:
            time = time_match.group(1)

        return {
            "intent": "calendar",
            "action": "create",
            "entities": {
                "title": user_input,
                "date": date,
                "time": time
            },
            "confidence": 1.0
        }