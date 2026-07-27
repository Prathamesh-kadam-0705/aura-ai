"""
Application service for the `Memory` domain entity.

This is the single orchestration point between:
  - inbound Pydantic schemas (memory/schemas/)
  - the persistence abstraction (memory/repositories/)
  - the ORM entity (memory/models/)

Routes (not yet generated) call this service; they never touch the
repository or the ORM model directly. This keeps business rules
(defaults, archive/pin semantics, access tracking) in exactly one place.
"""
from __future__ import annotations

import uuid
from typing import Optional, Sequence

from app.memory.models.enums import MemoryType
from app.memory.models.memory import Memory
from app.memory.repositories.base import AbstractMemoryRepository
from app.memory.schemas.memory import (
    MemoryCreate,
    MemoryRead,
    MemorySummary,
    MemoryUpdate,
)
from app.memory.services.exceptions import (
    MemoryNotFoundError,
    MemoryOperationNotAllowedError,
)


class MemoryService:
    """Coordinates validated memory operations on behalf of callers."""

    def __init__(self, repository: AbstractMemoryRepository) -> None:
        self._repository = repository

    async def create_memory(self, payload: MemoryCreate) -> MemoryRead:
        memory = Memory(
            user_id=payload.user_id,
            memory_type=payload.memory_type,
            title=payload.title,
            content=payload.content,
            summary=payload.summary,
            metadata_=payload.metadata_,
            importance_score=payload.importance_score,
            confidence_score=payload.confidence_score,
            embedding_id=payload.embedding_id,
            source=payload.source,
            tags=payload.tags,
            is_pinned=payload.is_pinned,
            is_archived=payload.is_archived,
        )
        created = await self._repository.create(memory)
        return MemoryRead.model_validate(created)

    async def get_memory(
        self, memory_id: uuid.UUID, user_id: uuid.UUID
    ) -> MemoryRead:
        memory = await self._repository.get_by_id(memory_id, user_id)
        if memory is None:
            raise MemoryNotFoundError(memory_id, user_id)
        return MemoryRead.model_validate(memory)

    async def list_memories(
        self,
        user_id: uuid.UUID,
        *,
        memory_type: Optional[MemoryType] = None,
        is_pinned: Optional[bool] = None,
        is_archived: Optional[bool] = None,
        tags: Optional[Sequence[str]] = None,
        min_importance: Optional[float] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[MemorySummary]:
        memories = await self._repository.list_by_user(
            user_id,
            memory_type=memory_type,
            is_pinned=is_pinned,
            is_archived=is_archived,
            tags=tags,
            min_importance=min_importance,
            limit=limit,
            offset=offset,
        )
        return [MemorySummary.model_validate(m) for m in memories]

    async def update_memory(
        self,
        memory_id: uuid.UUID,
        user_id: uuid.UUID,
        payload: MemoryUpdate,
    ) -> MemoryRead:
        values = payload.model_dump(exclude_unset=True, by_alias=False)

        # Guard against renaming metadata_ -> metadata mismatch on the ORM side.
        if "metadata_" in values:
            values["metadata_"] = values.pop("metadata_")

        updated = await self._repository.update(memory_id, user_id, values)
        if updated is None:
            raise MemoryNotFoundError(memory_id, user_id)
        return MemoryRead.model_validate(updated)

    async def delete_memory(self, memory_id: uuid.UUID, user_id: uuid.UUID) -> None:
        deleted = await self._repository.delete(memory_id, user_id)
        if not deleted:
            raise MemoryNotFoundError(memory_id, user_id)

    async def pin_memory(
        self, memory_id: uuid.UUID, user_id: uuid.UUID
    ) -> MemoryRead:
        memory = await self._repository.get_by_id(memory_id, user_id)
        if memory is None:
            raise MemoryNotFoundError(memory_id, user_id)
        if memory.is_archived:
            raise MemoryOperationNotAllowedError(
                "Cannot pin a memory that is archived. Unarchive it first."
            )
        updated = await self._repository.update(
            memory_id, user_id, {"is_pinned": True}
        )
        return MemoryRead.model_validate(updated)

    async def unpin_memory(
        self, memory_id: uuid.UUID, user_id: uuid.UUID
    ) -> MemoryRead:
        updated = await self._repository.update(
            memory_id, user_id, {"is_pinned": False}
        )
        if updated is None:
            raise MemoryNotFoundError(memory_id, user_id)
        return MemoryRead.model_validate(updated)

    async def archive_memory(
        self, memory_id: uuid.UUID, user_id: uuid.UUID
    ) -> MemoryRead:
        memory = await self._repository.get_by_id(memory_id, user_id)
        if memory is None:
            raise MemoryNotFoundError(memory_id, user_id)
        if memory.is_pinned:
            raise MemoryOperationNotAllowedError(
                "Cannot archive a pinned memory. Unpin it first."
            )
        updated = await self._repository.update(
            memory_id, user_id, {"is_archived": True}
        )
        return MemoryRead.model_validate(updated)

    async def unarchive_memory(
        self, memory_id: uuid.UUID, user_id: uuid.UUID
    ) -> MemoryRead:
        updated = await self._repository.update(
            memory_id, user_id, {"is_archived": False}
        )
        if updated is None:
            raise MemoryNotFoundError(memory_id, user_id)
        return MemoryRead.model_validate(updated)

    async def touch_memory(
        self, memory_id: uuid.UUID, user_id: uuid.UUID
    ) -> MemoryRead:
        """
        Record that a memory was retrieved/used by the reasoning engine
        (not yet generated). Increments `access_count` and stamps
        `last_accessed` — used later for recency-weighted retrieval ranking.
        """
        updated = await self._repository.record_access(memory_id, user_id)
        if updated is None:
            raise MemoryNotFoundError(memory_id, user_id)
        return MemoryRead.model_validate(updated)

    async def count_memories(
        self,
        user_id: uuid.UUID,
        *,
        memory_type: Optional[MemoryType] = None,
        is_archived: Optional[bool] = None,
    ) -> int:
        return await self._repository.count_by_user(
            user_id, memory_type=memory_type, is_archived=is_archived
        )