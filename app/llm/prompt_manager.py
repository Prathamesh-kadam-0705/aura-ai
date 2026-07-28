class PromptManager:


    @staticmethod
    def missing_entity_prompt(request, missing):

        return f"""
You are AURA.

The user wants to perform this action:

Intent: {request.intent}
Action: {request.action}

Missing information:
{", ".join(missing)}


Your task:
Ask the user a natural friendly question to get this missing information.


Important rules:
- Never mention "missing field".
- Never mention technical words.
- Never explain anything.
- Return only the question.
- One sentence only.


Examples:

If missing information is:
time

Answer:
What time should I set the alarm for?


If missing information is:
task

Answer:
What should I remind you about?


Now generate only the question.
"""