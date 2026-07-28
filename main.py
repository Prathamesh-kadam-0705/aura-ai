from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.core.cognitive_engine import CognitiveEngine
from app.core.orchestrator import Orchestrator

print("MAIN.PY LOADED")

app = FastAPI(title="AURA AI")

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = CognitiveEngine()
orchestrator = Orchestrator()


class ChatRequest(BaseModel):
    message: str


@app.post("/process")
def process(request: ChatRequest):
    print(f"request : {request}")
    request_object = engine.process(request.message)
    print(f"REQUEST OBJECT: {request_object}")
    response = orchestrator.process(request_object)
    print(f"RESPONSE: {response}")
    return response