from app.llm.local_llm import LocalLLM

llm = LocalLLM()

response = llm.understand(
    "Remind me to call Rahul tomorrow at 5 PM"
)

print(response)