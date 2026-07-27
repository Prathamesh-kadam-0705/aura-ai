class ActionRouter:

    def route(self, intent: str, user_input: str):

        text = user_input.lower()

        # ==========================
        # DEVICE
        # ==========================

        if intent == "device":

            if text.startswith("open "):
                return "open"

            if text.startswith("close "):
                return "close"

        # ==========================
        # REMINDER
        # ==========================

        if intent == "reminder":

            if "show" in text or "list" in text:
                return "list"

            if "delete" in text:
                return "delete"

            if "update" in text:
                return "update"

            return "create"

        # ==========================
        # NOTES
        # ==========================

        if intent == "notes":

            if "show" in text or "list" in text:
                return "read"

            if "delete" in text:
                return "delete"

            if "update" in text:
                return "update"

            return "create"

        # ==========================
        # TODO
        # ==========================

        if intent == "todo":

            if "show" in text or "list" in text:
                return "list"

            if "delete" in text:
                return "delete"

            if "update" in text:
                return "update"

            return "create"

        # ==========================
        # CONTACTS
        # ==========================

        if intent == "contacts":

            if "show" in text or "list" in text:
                return "list"

            if "find" in text or "search" in text:
                return "search"

            if "delete" in text:
                return "delete"

            if "update" in text:
                return "update"

            return "create"

        # ==========================
        # MEMORY
        # ==========================

        if intent == "memory":

            if text.startswith("what"):
                return "read"

            if text.startswith("when"):
                return "read"

            return "create"

        # ==========================
        # WEATHER
        # ==========================

        if intent == "weather":
            return "read"

        # ==========================
        # ALARM
        # ==========================

        if intent == "alarm":

            if "delete" in text:
                return "delete"

            if "show" in text:
                return "list"

            return "create"

        return None