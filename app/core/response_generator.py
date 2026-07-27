class ResponseGenerator:

    @staticmethod
    def success(
        answer: str,
        message: str = "Success",
        payload: dict | None = None
    ):
        return {
            "success": True,
            "message": message,
            "data": {
                "answer": answer,
                "payload": payload or {}
            }
        }

    @staticmethod
    def error(message: str):
        return {
            "success": False,
            "message": message,
            "data": {
                "answer": message,
                "payload": {}
            }
        }