from app.database.session import SessionLocal
from app.database.models.alarm import Alarm

from app.services.datetime_parser import DateTimeParser


class AlarmModule:


    def create(self, request):

        db = SessionLocal()

        try:

            alarm = Alarm(

                time=DateTimeParser.parse_time(
                    request.entities.get("time")
                ),

                label=request.entities.get(
                    "label"
                )

            )


            db.add(alarm)

            db.commit()

            db.refresh(alarm)


            return {

                "success": True,

                "message": "Alarm created successfully.",

                "data": {

                    "id": alarm.id,

                    "time": str(alarm.time),

                    "label": alarm.label,

                    "enabled": alarm.enabled

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

        db = SessionLocal()

        try:

            alarms = db.query(Alarm).all()


            data=[]


            for alarm in alarms:

                data.append({

                    "id":alarm.id,

                    "time":str(alarm.time),

                    "label":alarm.label,

                    "enabled":alarm.enabled

                })


            return {

                "success":True,

                "data":data

            }


        finally:

            db.close()



    def delete(self, request):

        db = SessionLocal()

        try:

            alarm_id=request.entities.get("id")


            alarm=db.query(Alarm).filter(
                Alarm.id==alarm_id
            ).first()


            if alarm is None:

                return {

                    "success":False,

                    "message":"Alarm not found."

                }


            db.delete(alarm)

            db.commit()


            return {

                "success":True,

                "message":"Alarm deleted."

            }


        finally:

            db.close()