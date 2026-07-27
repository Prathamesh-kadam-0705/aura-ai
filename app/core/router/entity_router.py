import re


class EntityRouter:

    def route(self, intent: str, action: str, user_input: str):

        text = user_input.lower()


        # ======================
        # DEVICE
        # ======================

        if intent == "device":

            if action in ["open", "close"]:

                return {
                    "app": user_input.split(" ", 1)[1].strip()
                }



        # ======================
        # ALARM
        # ======================

        if intent == "alarm":

            time_match = re.search(
                r'(\d{1,2}(:\d{2})?\s?(am|pm))',
                user_input,
                re.IGNORECASE
            )

            return {
                "time": time_match.group(1) if time_match else None
            }



        # ======================
        # WEATHER
        # ======================

        if intent == "weather":

            location = None

            if " in " in text:

                location = user_input.split(" in ", 1)[1].strip()


            return {
                "location": location
            }



        # ======================
        # REMINDER
        # ======================

        if intent == "reminder":

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



            task = text


            remove_words = [

                "remind me to",
                "reminder",
                "set reminder",
                "create reminder",
                "tomorrow",
                "today"

            ]


            for word in remove_words:

                task = task.replace(word, "")



            return {

                "task": task.strip(),
                "date": date,
                "time": time

            }



        # ======================
        # MEMORY
        # ======================

        if intent == "memory":


            # CREATE MEMORY

            if action == "create":


                if "my name is" in text:

                    return {

                        "category": "personal",
                        "key": "name",
                        "value": text.split("is", 1)[1].strip()

                    }



                if "my birthday is" in text:

                    return {

                        "category": "personal",
                        "key": "birthday",
                        "value": text.split("is", 1)[1].strip()

                    }



                if "my favorite color is" in text:

                    return {

                        "category": "personal",
                        "key": "favorite_color",
                        "value": text.split("is", 1)[1].strip()

                    }



            # READ MEMORY

            if action == "read":


                if "favorite color" in text:

                    return {

                        "key": "favorite_color"

                    }



                if "birthday" in text:

                    return {

                        "key": "birthday"

                    }



                if "name" in text:

                    return {

                        "key": "name"

                    }



        # ======================
        # UNKNOWN
        # ======================

        return {}