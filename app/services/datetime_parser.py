from datetime import datetime


class DateTimeParser:


    @staticmethod
    def parse_time(value):

        if not value:
            return None


        formats = [
            "%I:%M %p",
            "%I %p",
            "%H:%M",
            "%H"
        ]


        for fmt in formats:

            try:

                return datetime.strptime(
                    value,
                    fmt
                ).time()

            except:

                pass


        return None



    @staticmethod
    def parse_date(value):

        if not value:
            return None


        value=value.lower()


        if value=="tomorrow":

            from datetime import date,timedelta

            return date.today()+timedelta(days=1)


        if value=="today":

            from datetime import date

            return date.today()


        return None