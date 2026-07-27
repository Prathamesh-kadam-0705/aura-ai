class DeviceModule:


    def open(self, request):

        app = request.entities.get("app")


        if not app:
            return {
                "success":False,
                "message":"App name missing"
            }


        return {
            "success":True,
            "message":f"{app} open command generated.",
            "data":{
                "action":"open_app",
                "app":app
            }
        }



    def close(self, request):

        app = request.entities.get("app")


        if not app:
            return {
                "success":False,
                "message":"App name missing"
            }


        return {
            "success":True,
            "message":f"{app} close command generated.",
            "data":{
                "action":"close_app",
                "app":app
            }
        }