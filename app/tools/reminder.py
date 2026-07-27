from app.database.session import SessionLocal
from app.database.models.reminder import Reminder
from app.services.datetime_parser import DateTimeParser


class ReminderModule:

    def create(self, request):

        db = SessionLocal()

        try:
            task = request.entities.get("task")
            date = DateTimeParser.parse_date(
                request.entities.get("date")
            )
            time = DateTimeParser.parse_time(
                request.entities.get("time")
            )

            reminder = Reminder(
                task=task,
                date=date,
                time=time
            )

            db.add(reminder)
            db.commit()
            db.refresh(reminder)

            return {
                "id": reminder.id,
                "task": reminder.task,
                "date": str(reminder.date) if reminder.date else None,
                "time": str(reminder.time) if reminder.time else None,
                "status": reminder.status,
            }

        except Exception as e:

            db.rollback()

            return {
                "success": False,
                "message": str(e)
            }

        finally:
            db.close()


    def update(self, request):

        reminder_id = request.entities.get("id")

        db = SessionLocal()

        try:

            reminder = db.query(Reminder).filter(
                Reminder.id == reminder_id
            ).first()

            if reminder is None:
                return {
                    "success": False,
                    "message": "Reminder not found."
                }

            reminder.task = request.entities.get(
                "task",
                reminder.task
            )

            if request.entities.get("date"):
                reminder.date = DateTimeParser.parse_date(
                    request.entities["date"]
                )

            if request.entities.get("time"):
                reminder.time = DateTimeParser.parse_time(
                    request.entities["time"]
                )

            db.commit()
            db.refresh(reminder)

            return {
                "id": reminder.id,
                "task": reminder.task,
                "date": str(reminder.date) if reminder.date else None,
                "time": str(reminder.time) if reminder.time else None,
                "status": reminder.status,
            }
        except Exception as e:

            db.rollback()

            return {
                "success": False,
                "message": str(e)
            }

        finally:
            db.close()

    def delete(self, request):

        reminder_id = request.entities.get("id")

        db = SessionLocal()

        try:

            reminder = db.query(Reminder).filter(
                Reminder.id == reminder_id
            ).first()

            if reminder is None:
                return {
                    "success": False,
                    "message": "Reminder not found."
                }

            db.delete(reminder)
            db.commit()

            return {
                "deleted": True,
                "id": reminder_id
            }

        except Exception as e:

            db.rollback()

            return {
                "success": False,
                "message": str(e)
            }

        finally:
            db.close()


    def list(self, request):

        db = SessionLocal()

        try:

            reminders = db.query(Reminder).all()

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

        finally:
            db.close()

    def read(self, request):
        return self.list(request)