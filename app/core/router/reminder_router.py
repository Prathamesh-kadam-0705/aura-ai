import re


class ReminderRouter:

    def route(self, user_input: str):

        text = user_input.lower()

        # CREATE
        if "remind me" in text:

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

            task = (
                text
                .replace("remind me to", "")
                .replace("tomorrow", "")
                .replace("today", "")
                .strip()
            )

            return {
                "intent": "reminder",
                "action": "create",
                "entities": {
                    "task": task,
                    "date": date,
                    "time": time
                },
                "confidence": 1.0
            }

        # LIST
        if "show reminders" in text or "all reminders" in text:

            return {
                "intent": "reminder",
                "action": "list",
                "entities": {},
                "confidence": 1.0
            }

        return None