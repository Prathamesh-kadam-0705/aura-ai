class WeatherModule:


    def read(self, request):

        location = request.entities.get("location")


        if not location:

            return {
                "success":False,
                "message":"Location missing"
            }


        # temporary response
        # later connect weather API

        return {

            "success":True,

            "message":"Weather data fetched successfully.",

            "data":{

                "location":location,

                "temperature":"28°C",

                "condition":"Clear sky"

            }

        }