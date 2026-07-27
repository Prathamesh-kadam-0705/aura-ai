from app.database.session import SessionLocal
from app.database.models.calendar import Calendar
from app.services.datetime_parser import DateTimeParser


class CalendarModule:


    def create(self, request):

        db = SessionLocal()

        try:

            event = Calendar(

                title=request.entities.get("title"),

                date=DateTimeParser.parse_date(
                    request.entities.get("date")
                ),

                time=DateTimeParser.parse_time(
                    request.entities.get("time")
                ),

                location=request.entities.get("location")

            )


            db.add(event)
            db.commit()
            db.refresh(event)


            return {

                "success":True,

                "message":"Event created successfully.",

                "data":{

                    "id":event.id,

                    "title":event.title,

                    "date":str(event.date),

                    "time":str(event.time) if event.time else None,

                    "location":event.location

                }

            }


        except Exception as e:

            db.rollback()

            return {
                "success":False,
                "message":str(e)
            }


        finally:

            db.close()



    def list(self, request):

        db=SessionLocal()

        try:

            events=db.query(Calendar).all()


            data=[]


            for event in events:

                data.append({

                    "id":event.id,

                    "title":event.title,

                    "date":str(event.date),

                    "time":str(event.time) if event.time else None,

                    "location":event.location

                })


            return {

                "success":True,

                "data":data

            }


        finally:

            db.close()