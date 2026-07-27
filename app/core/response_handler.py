from app.core.response_generator import ResponseGenerator


class ResponseHandler:

    def build(self, request, result):

        if request.intent == "conversation":

            return ResponseGenerator.success(
                answer=result["answer"],
                message="Conversation completed.",
                payload=result
            )

        if request.intent == "reminder":

            if request.action == "create":

                return ResponseGenerator.success(
                    answer=f"Reminder created for '{result['task']}'.",
                    message="Reminder created successfully.",
                    payload=result
                )

            if request.action == "update":

                return ResponseGenerator.success(
                    answer="Reminder updated successfully.",
                    payload=result
                )

            if request.action == "delete":

                return ResponseGenerator.success(
                    answer="Reminder deleted successfully.",
                    payload=result
                )

            if request.action in ["read", "list"]:

                return ResponseGenerator.success(
                    answer=f"You have {len(result)} reminders.",
                    payload=result
                )

            if request.intent == "alarm":

                if request.action == "create":

                    alarm = result["data"]

                    return ResponseGenerator.success(

                        answer=f"Alarm set for {alarm['time']}.",

                        message="Alarm created successfully.",

                        payload=alarm

                    )


                if request.action == "delete":

                    return ResponseGenerator.success(

                        answer="Alarm deleted successfully.",

                        payload=result

                    )


                if request.action in ["read", "list"]:

                    alarms = result["data"]

                    return ResponseGenerator.success(

                        answer=f"You have {len(alarms)} alarms.",

                        payload=alarms

                    )

        return ResponseGenerator.success(
            answer="Done.",
            payload=result
        )