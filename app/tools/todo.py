from app.database.session import SessionLocal
from app.database.models.todo import Todo


class TodoModule:


    def create(self, request):

        db = SessionLocal()

        try:

            todo = Todo(
                task=request.entities.get("task")
            )

            db.add(todo)
            db.commit()
            db.refresh(todo)

            return {
                "success": True,
                "message": "Todo created successfully.",
                "data": {
                    "id": todo.id,
                    "task": todo.task,
                    "completed": todo.completed
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



    def list(self, request):

        db = SessionLocal()

        try:

            todos = db.query(Todo).all()

            data = []

            for todo in todos:

                data.append({
                    "id": todo.id,
                    "task": todo.task,
                    "completed": todo.completed
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

            todo_id = request.entities.get("id")
            task = request.entities.get("task")


            todo = db.query(Todo).filter(
                Todo.id == todo_id
            ).first()


            if todo is None:

                return {
                    "success": False,
                    "message": "Todo not found."
                }


            if task:
                todo.task = task


            if "completed" in request.entities:

                todo.completed = request.entities.get(
                    "completed"
                )


            db.commit()


            return {
                "success": True,
                "message": "Todo updated successfully."
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

            task = request.entities.get("task")


            todo = db.query(Todo).filter(
                Todo.task == task
            ).first()


            if todo is None:

                return {
                    "success": False,
                    "message": "Todo not found."
                }


            db.delete(todo)
            db.commit()


            return {
                "success": True,
                "message": "Todo deleted successfully."
            }


        finally:
            db.close()