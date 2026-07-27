from ollama import chat
from app.llm.prompts import SYSTEM_PROMPT
import json


class LocalLLM:

    def __init__(self):
        self.model = "llama3.2:1b"

    def understand(self, user_input: str):

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        content = response.message.content.strip()

        print("========== RAW LLM ==========")
        print(content)
        print("=============================")

        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        try:
            # First parse
            parsed = json.loads(content)

            # If the model returned a JSON string, parse again
            if isinstance(parsed, str):
                parsed = json.loads(parsed)

            def clean(obj):
                if isinstance(obj, dict):
                    return {
                        str(k).strip(): clean(v)
                        for k, v in obj.items()
                    }
                elif isinstance(obj, list):
                    return [clean(i) for i in obj]
                elif isinstance(obj, str):
                    return obj.strip()
                else:
                    return obj

            parsed = clean(parsed)

            print("FINAL TYPE:", type(parsed))
            print("FINAL:", parsed)

            return parsed

        except Exception as e:
            print("JSON ERROR:", e)

            return {
                "intent": "general",
                "action": "answer",
                "entities": {
                    "topic": user_input
                },
                "confidence": 0.5
            }