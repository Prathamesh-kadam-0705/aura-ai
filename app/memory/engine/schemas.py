"""
Pydantic v2 schemas for the retrieval engine's public contract.
"""
from __future__ import annotations

import uuid
from typing import Optional

from pydantic import Field

from app.memory.models.enums import MemoryType
from app.memory.schemas.base import ORMBaseSchema, StrictBaseSchema
from app.memory.schemas.memory import MemorySummary


class RetrievalRequest(StrictBaseSchema):
    """A request to retrieve the most relevant memories for a given query."""

    user_id: uuid.UUID
    query_vector: list[float] = Field(min_length=1)
    top_k: int = Field(default=10, ge=1, le=50)
    memory_type: Optional[MemoryType] = None
    record_access: bool = Field(
        default=True,
        description="If true, retrieved memories have access_count "
        "incremented and last_accessed stamped.",
    )


class RankedMemory(ORMBaseSchema):
    """A single retrieval result with its constituent and final scores."""

    memory: MemorySummary
    similarity_score: float
    """1.0 - cosine_distance; higher is more similar."""
    recency_score: float
    final_score: float


class RetrievalResult(ORMBaseSchema):
    """The full response for a retrieval request."""

    user_id: uuid.UUID
    results: list[RankedMemory]
    total_candidates_considered: int