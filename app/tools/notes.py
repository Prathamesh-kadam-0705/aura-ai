from app.database.session import SessionLocal
from app.database.models.note import Note


class NoteModule:

    def create(self, request):

        db = SessionLocal()

        try:

            note = Note(
                title=request.entities.get("title"),
                content=request.entities.get("content")
            )

            db.add(note)
            db.commit()
            db.refresh(note)

            return {
                "success": True,
                "message": "Note created successfully.",
                "data": {
                    "id": note.id,
                    "title": note.title,
                    "content": note.content
                }
            }

        except Exception as e:

            db.rollback()

            return {
                "success": False,
                "message": str(e)
            }

        finally:
            db.close()

    def read(self, request):

        db = SessionLocal()

        try:

            note_id = request.entities.get("id")
            title = request.entities.get("title")

            query = db.query(Note)

            if note_id:
                query = query.filter(Note.id == note_id)

            elif title:
                query = query.filter(Note.title == title)

            notes = query.all()

            data = []

            for note in notes:
                data.append({
                    "id": note.id,
                    "title": note.title,
                    "content": note.content
                })

            return {
                "success": True,
                "data": data
            }

        finally:
            db.close()

    def update(self, request):

        db = SessionLocal()

        try:

            note_id = request.entities.get("id")

            note = db.query(Note).filter(
                Note.id == note_id
            ).first()

            if note is None:
                return {
                    "success": False,
                    "message": "Note not found."
                }

            if request.entities.get("title"):
                note.title = request.entities.get("title")

            if request.entities.get("content"):
                note.content = request.entities.get("content")

            db.commit()

            return {
                "success": True,
                "message": "Note updated successfully."
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

        db = SessionLocal()

        try:

            note_id = request.entities.get("id")

            note = db.query(Note).filter(
                Note.id == note_id
            ).first()

            if note is None:
                return {
                    "success": False,
                    "message": "Note not found."
                }

            db.delete(note)
            db.commit()

            return {
                "success": True,
                "message": "Note deleted successfully."
            }

        except Exception as e:

            db.rollback()

            return {
                "success": False,
                "message": str(e)
            }

        finally:
            db.close()