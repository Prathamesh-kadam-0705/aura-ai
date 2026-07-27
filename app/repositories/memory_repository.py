from database.session import SessionLocal
from database.models.memory import Memory


class MemoryRepository:

    def get_by_key(self, key: str):
        db = SessionLocal()
        try:
            return db.query(Memory).filter(
                Memory.key == key
            ).first()
        finally:
            db.close()

    def create(self, category, key, value):
        db = SessionLocal()

        try:
            memory = Memory(
                category=category,
                key=key,
                value=value
            )

            db.add(memory)
            db.commit()
            db.refresh(memory)

            return memory

        except:
            db.rollback()
            raise

        finally:
            db.close()

    def update(self, memory, category, value):
        db = SessionLocal()

        try:
            obj = db.merge(memory)

            obj.category = category
            obj.value = value

            db.commit()
            db.refresh(obj)

            return obj

        except:
            db.rollback()
            raise

        finally:
            db.close()

    def delete(self, key):

        db = SessionLocal()

        try:

            memory = db.query(Memory).filter(
                Memory.key == key
            ).first()

            if memory:
                db.delete(memory)
                db.commit()

            return memory

        finally:
            db.close()