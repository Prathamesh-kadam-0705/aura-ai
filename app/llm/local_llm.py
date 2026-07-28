from ollama import chat
from app.llm.prompts import SYSTEM_PROMPT
from app.llm.prompt_manager import PromptManager

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

        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        try:

            parsed = json.loads(content)

            if isinstance(parsed, str):
                parsed = json.loads(parsed)


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



    def generate_missing_question(self, request, missing):

        prompt = PromptManager.missing_entity_prompt(
            request,
            missing
        )

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0.2
            }
        )

        answer = response.message.content.strip()

        answer = answer.replace("assistant", "")
        answer = answer.replace('"', "")
        answer = answer.strip()

        return answer