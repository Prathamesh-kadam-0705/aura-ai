from pydantic import BaseModel
from typing import Dict


class Request(BaseModel):
    intent: str
    action: str
    entities: Dict = {}
    confidence: float = 0.0