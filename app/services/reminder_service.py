from database.models.reminder import Reminder
from app.repositories.reminder_repository import ReminderRepository
from app.services.datetime_parser import DateTimeParser


class ReminderService:

    def __init__(self):
        self.repository = ReminderRepository()

    def create(self, request):

        reminder = Reminder(
            task=request.entities.get("task"),
            date=DateTimeParser.parse_date(
                request.entities.get("date")
            ),
            time=DateTimeParser.parse_time(
                request.entities.get("time")
            )
        )

        reminder = self.repository.create(reminder)

        return {
            "success": True,
            "message": "Reminder created successfully.",
            "data": {
                "id": reminder.id,
                "task": reminder.task,
                "date": str(reminder.date) if reminder.date else None,
                "time": str(reminder.time) if reminder.time else None,
                "status": reminder.status
            }
        }

    def list(self):

        reminders = self.repository.get_all()

        data = []

        for reminder in reminders:
            data.append({
                "id": reminder.id,
                "task": reminder.task,
                "date": str(reminder.date) if reminder.date else None,
                "time": str(reminder.time) if reminder.time else None,
                "status": reminder.status
            })

        return {
            "success": True,
            "message": "Reminders fetched successfully.",
            "data": data
        }