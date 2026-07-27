from app.database.session import SessionLocal
from app.database.models.memory import Memory


class MemoryModule:

    def create(self, request):

        db = SessionLocal()

        print("CREATE MEMORY")
        print(request.entities)         


        try:

            key = request.entities.get("key")

            memory = db.query(Memory).filter(
                Memory.key == key
            ).first()

            if memory:

                memory.value = request.entities.get("value")
                memory.category = request.entities.get("category")

                db.commit()
                db.refresh(memory)

                return {
                    "success": True,
                    "message": "Memory updated successfully.",
                    "data": {
                        "id": memory.id,
                        "category": memory.category,
                        "key": memory.key,
                        "value": memory.value
                    }
                }

            memory = Memory(
                category=request.entities.get("category"),
                key=key,
                value=request.entities.get("value")
            )

            db.add(memory)
            db.commit()
            db.refresh(memory)
           
            return {
                "success": True,
                "message": "Memory saved successfully.",
                "data": {
                    "id": memory.id,
                    "category": memory.category,
                    "key": memory.key,
                    "value": memory.value
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

        print("READ MEMORY")
        print(request.entities)

        try:

            key = request.entities.get("key")

            memory = db.query(Memory).filter(
                Memory.key == key
            ).first()

            if memory is None:

                return {
                    "success": False,
                    "message": "Memory not found."
                }

            return {
                "success": True,
                "data": {
                    "category": memory.category,
                    "key": memory.key,
                    "value": memory.value
                }
            }

        finally:
            db.close()

    def update(self, request):

        db = SessionLocal()

        print("UPDATE MEMORY")
        print(request.entities)
        
        try:

            key = request.entities.get("key")

            memory = db.query(Memory).filter(
                Memory.key == key
            ).first()

            if memory is None:

                return {
                    "success": False,
                    "message": "Memory not found."
                }

            memory.value = request.entities.get(
                "value",
                memory.value
            )

            db.commit()

            return {
                "success": True,
                "message": "Memory updated successfully."
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

            key = request.entities.get("key")

            memory = db.query(Memory).filter(
                Memory.key == key
            ).first()

            if memory is None:

                return {
                    "success": False,
                    "message": "Memory not found."
                }

            db.delete(memory)

            db.commit()

            return {
                "success": True,
                "message": "Memory deleted successfully."
            }

        except Exception as e:

            db.rollback()

            return {
                "success": False,
                "message": str(e)
            }

        finally:
            db.close()