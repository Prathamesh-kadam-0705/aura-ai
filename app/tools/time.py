from datetime import datetime


class TimeTool:


    def read(self, request):

        today = datetime.now()

        return {
            "success": True,
            "message": "Today's date",
            "data": {
                "date": today.strftime("%d %B %Y"),
                "day": today.strftime("%A")
            }
        }