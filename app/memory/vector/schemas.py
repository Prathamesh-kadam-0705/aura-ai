"""
Pydantic v2 schemas for the vector store integration layer.

These are intentionally decoupled from `memory/schemas/memory.py` — the
vector store is a distinct bounded concern (similarity search), not a
CRUD resource, and should be free to evolve independently.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import Field, field_validator

from app.memory.schemas.base import ORMBaseSchema, StrictBaseSchema

DEFAULT_EMBEDDING_DIMENSIONS = 1536


class VectorUpsertRequest(StrictBaseSchema):
    """Payload to create or replace the embedding for a given memory."""

    memory_id: uuid.UUID
    user_id: uuid.UUID
    vector: list[float] = Field(min_length=1)
    model_name: str = Field(max_length=128)

    @field_validator("vector")
    @classmethod
    def _check_finite(cls, value: list[float]) -> list[float]:
        for component in value:
            if component != component:  # NaN check without importing math
                raise ValueError("vector components must not be NaN")
        return value


class VectorQueryRequest(StrictBaseSchema):
    """Payload to perform a similarity search scoped to a single user."""

    user_id: uuid.UUID
    query_vector: list[float] = Field(min_length=1)
    top_k: int = Field(default=10, ge=1, le=100)
    max_distance: Optional[float] = Field(default=None, ge=0.0)


class VectorRecordRead(ORMBaseSchema):
    """Full representation of a stored embedding record."""

    id: uuid.UUID
    memory_id: uuid.UUID
    user_id: uuid.UUID
    model_name: str
    dimensions: int
    created_at: datetime


class VectorSearchResult(ORMBaseSchema):
    """A single similarity search hit."""

    embedding_id: uuid.UUID
    memory_id: uuid.UUID
    distance: float