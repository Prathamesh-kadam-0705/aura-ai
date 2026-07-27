import re

from app.core.rules.alarm_rules import ALARM_RULES
from app.core.rules.device_rules import DEVICE_RULES
from app.core.rules.weather_rules import WEATHER_RULES
from app.core.rules.reminder_rules import REMINDER_RULES
from app.core.rules.memory_rules import MEMORY_RULES
from app.core.rules.calendar_rules import CALENDAR_RULES
from app.core.rules.contacts_rules import CONTACTS_RULES
from app.core.rules.notes_rules import NOTES_RULES
from app.core.rules.todo_rules import TODO_RULES


class IntentRouter:

    def __init__(self):

        self.rules = [

            ALARM_RULES,
            DEVICE_RULES,
            WEATHER_RULES,
            REMINDER_RULES,
            MEMORY_RULES,
            CALENDAR_RULES,
            CONTACTS_RULES,
            NOTES_RULES,
            TODO_RULES

        ]

        self.greetings = [
            "hi",
            "hello",
            "hey",
            "hi aura",
            "hello aura",
            "hey aura",
            "good morning",
            "good afternoon",
            "good evening"
        ]


    def route(self, user_input):

        text = user_input.lower().strip()


        # 1. Greeting Detection
        for greeting in self.greetings:

            if text == greeting or text.startswith(greeting):

                return {
                    "intent": "conversation",
                    "action": "greeting",
                    "entities": {},
                    "confidence": 1.0
                }


        # 2. Feature Rules
        for rule in self.rules:

            for pattern in rule["patterns"]:

                if re.match(pattern["pattern"], text):

                    return {
                        "intent": rule["intent"],
                        "action": pattern["action"],
                        "entities": {},
                        "confidence": 1.0
                    }


        # 3. Unknown Conversation
        return None