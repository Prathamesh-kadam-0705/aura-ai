class VoiceModule:


    def speak(self, request):

        text = request.entities.get("text")


        return {
            "success": True,
            "message": "Voice generated successfully.",
            "data": {
                "text": text,
                "status": "ready"
            }
        }



    def listen(self, request):

        return {
            "success": True,
            "message": "Listening started.",
            "data": {
                "status": "listening"
            }
        }