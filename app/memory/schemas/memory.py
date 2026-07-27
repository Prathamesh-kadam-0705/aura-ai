"""
Pydantic v2 schemas for the `Memory` domain entity.

These schemas define the contract between the Memory Engine's internal
layers (repositories/services, not yet generated) and any external
consumer (API routes, not yet generated). This module has no dependency
on FastAPI, SQLAlchemy sessions, or routing — it is pure data contract.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import Field, field_validator

from app.memory.models.enums import MemoryType
from app.memory.schemas.base import ORMBaseSchema, StrictBaseSchema

# --- Shared field constraints -------------------------------------------

_TITLE_MAX_LENGTH = 255
_SOURCE_MAX_LENGTH = 255
_EMBEDDING_ID_MAX_LENGTH = 255
_MAX_TAGS = 50
_TAG_MAX_LENGTH = 64


def _validate_tags(tags: list[str]) -> list[str]:
    if len(tags) > _MAX_TAGS:
        raise ValueError(f"tags cannot exceed {_MAX_TAGS} items")
    normalized: list[str] = []
    for tag in tags:
        cleaned = tag.strip()
        if not cleaned:
            raise ValueError("tags cannot contain empty strings")
        if len(cleaned) > _TAG_MAX_LENGTH:
            raise ValueError(f"each tag must be at most {_TAG_MAX_LENGTH} characters")
        normalized.append(cleaned)
    return normalized


# --- Create --------------------------------------------------------------

class MemoryCreate(StrictBaseSchema):
    """Payload required to create a new Memory record."""

    user_id: uuid.UUID
    memory_type: MemoryType
    title: Optional[str] = Field(default=None, max_length=_TITLE_MAX_LENGTH)
    content: str = Field(min_length=1)
    summary: Optional[str] = None
    metadata_: dict[str, Any] = Field(default_factory=dict, alias="metadata")
    importance_score: float = Field(default=0.5, ge=0.0, le=1.0)
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    embedding_id: Optional[str] = Field(
        default=None, max_length=_EMBEDDING_ID_MAX_LENGTH
    )
    source: Optional[str] = Field(default=None, max_length=_SOURCE_MAX_LENGTH)
    tags: list[str] = Field(default_factory=list)
    is_pinned: bool = False
    is_archived: bool = False

    @field_validator("tags")
    @classmethod
    def _check_tags(cls, value: list[str]) -> list[str]:
        return _validate_tags(value)


# --- Update ---------------------------------------------------------------

class MemoryUpdate(StrictBaseSchema):
    """
    Partial-update payload for an existing Memory record.

    Every field is optional; only fields explicitly supplied by the
    caller should be applied. `memory_type` and `user_id` are
    intentionally excluded — ownership and classification are immutable
    after creation and must be handled via new-memory creation instead.
    """

    title: Optional[str] = Field(default=None, max_length=_TITLE_MAX_LENGTH)
    content: Optional[str] = Field(default=None, min_length=1)
    summary: Optional[str] = None
    metadata_: Optional[dict[str, Any]] = Field(default=None, alias="metadata")
    importance_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    confidence_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    embedding_id: Optional[str] = Field(
        default=None, max_length=_EMBEDDING_ID_MAX_LENGTH
    )
    source: Optional[str] = Field(default=None, max_length=_SOURCE_MAX_LENGTH)
    tags: Optional[list[str]] = None
    is_pinned: Optional[bool] = None
    is_archived: Optional[bool] = None

    @field_validator("tags")
    @classmethod
    def _check_tags(cls, value: Optional[list[str]]) -> Optional[list[str]]:
        if value is None:
            return value
        return _validate_tags(value)


# --- Read (full representation) -------------------------------------------

class MemoryRead(ORMBaseSchema):
    """Full representation of a Memory record, as returned to callers."""

    id: uuid.UUID
    user_id: uuid.UUID
    memory_type: MemoryType
    title: Optional[str]
    content: str
    summary: Optional[str]
    metadata_: dict[str, Any] = Field(alias="metadata")
    importance_score: float
    confidence_score: float
    embedding_id: Optional[str]
    source: Optional[str]
    tags: list[str]
    is_pinned: bool
    is_archived: bool
    access_count: int
    last_accessed: Optional[datetime]
    created_at: datetime
    updated_at: datetime


# --- Read (lightweight summary, e.g. for list/search results) -------------

class MemorySummary(ORMBaseSchema):
    """
    Condensed representation for list views and retrieval results, where
    returning full `content` for every hit would be wasteful.
    """

    id: uuid.UUID
    memory_type: MemoryType
    title: Optional[str]
    summary: Optional[str]
    importance_score: float
    is_pinned: bool
    tags: list[str]
    created_at: datetime


# --- Internal access-tracking payload --------------------------------------

class MemoryAccessUpdate(StrictBaseSchema):
    """
    Internal payload for recording that a memory was retrieved/used.

    Kept separate from `MemoryUpdate` because access tracking is a
    system-driven side effect (incrementing `access_count`, stamping
    `last_accessed`), not a user-driven content edit.
    """

    accessed_at: datetime = Field(default_factory=datetime.utcnow)