from app.tools.reminder import ReminderModule
from app.tools.memory import MemoryModule
from app.tools.notes import NoteModule
from app.tools.todo import TodoModule
from app.tools.calendar import CalendarModule
from app.tools.alarm import AlarmModule 
from app.tools.contacts import ContactModule
from app.tools.device import DeviceModule
from app.tools.voice import VoiceModule
from app.tools.knowledge import KnowledgeModule
from app.tools.weather import WeatherModule
from app.tools.time import TimeTool


class ToolRegistry:

    def __init__(self):

        self.tools = {
            "reminder": ReminderModule(),
            "memory": MemoryModule(),
            "notes": NoteModule(),
            "todo": TodoModule(),
            "todo": TodoModule(),
            "calendar": CalendarModule(),
            "alarm": AlarmModule(),
            "contacts": ContactModule(),
            "device": DeviceModule(),
            "voice": VoiceModule(),
            "general": KnowledgeModule(),
            "weather": WeatherModule(),
            "general": TimeTool()
        }

    def get_tool(self, intent):
        return self.tools.get(intent)