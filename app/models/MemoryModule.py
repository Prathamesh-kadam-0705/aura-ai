from app.services.memory_service import MemoryService


class MemoryModule:

    def __init__(self):
        self.service = MemoryService()

    def create(self, request):
        return self.service.create(request)

    def read(self, request):
        return self.service.read(request)

    def delete(self, request):
        return self.service.delete(request)