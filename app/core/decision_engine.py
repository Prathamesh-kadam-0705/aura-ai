from app.registry.tool_registry import ToolRegistry


class DecisionEngine:

    def __init__(self):
        self.registry = ToolRegistry()

    def decide(self, request):

        tool = self.registry.get_tool(request.intent)

        if tool is None:
            return None

        return tool