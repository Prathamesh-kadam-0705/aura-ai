from app.services.reminder_service import ReminderService


class ReminderModule:

    def __init__(self):
        self.service = ReminderService()

    def create(self, request):
        return self.service.create(request)

    def list(self, request):
        return self.service.list()

    def read(self, request):
        return self.service.list()