import re


class ContactsRouter:

    def route(self, user_input: str):

        text = user_input.lower()

        if text.startswith("save"):

            phone = None

            phone_match = re.search(r'\d{10}', user_input)

            if phone_match:
                phone = phone_match.group()

            words = user_input.split()

            name = words[1] if len(words) > 1 else None

            return {
                "intent": "contacts",
                "action": "create",
                "entities": {
                    "name": name,
                    "phone": phone
                },
                "confidence": 1.0
            }

        if text.startswith("find"):

            return {
                "intent": "contacts",
                "action": "search",
                "entities": {
                    "name": user_input.replace("Find", "").replace("find", "").replace("contact", "").strip()
                },
                "confidence": 1.0
            }

        if "all contacts" in text:

            return {
                "intent": "contacts",
                "action": "list",
                "entities": {},
                "confidence": 1.0
            }

        return None