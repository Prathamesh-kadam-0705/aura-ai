from database.session import SessionLocal
from database.models.reminder import Reminder


class ReminderRepository:

    def create(self, reminder):

        db = SessionLocal()

        try:
            db.add(reminder)
            db.commit()
            db.refresh(reminder)
            return reminder

        finally:
            db.close()

    def get_all(self):

        db = SessionLocal()

        try:
            return db.query(Reminder).all()

        finally:
            db.close()

    def get_by_id(self, reminder_id):

        db = SessionLocal()

        try:
            return (
                db.query(Reminder)
                .filter(Reminder.id == reminder_id)
                .first()
            )

        finally:
            db.close()

    def update(self):

        db = SessionLocal()

        try:
            db.commit()

        finally:
            db.close()

    def delete(self, reminder):

        db = SessionLocal()

        try:
            db.delete(reminder)
            db.commit()

        finally:
            db.close()