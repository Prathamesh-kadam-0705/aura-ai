"""
Concrete async SQLAlchemy 2.0 repository for the `Memory` entity.

This is the only layer in the Memory Engine that is allowed to construct
SQL/ORM queries. Services (not yet generated) depend on
`AbstractMemoryRepository`, never on this class or on `AsyncSession`
directly, so the persistence technology can change without touching
business logic.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional, Sequence

from sqlalchemy import func, select, update as sa_update
from sqlalchemy.ext.asyncio import AsyncSession

from app.memory.models.enums import MemoryType
from app.memory.models.memory import Memory
from app.memory.repositories.base import AbstractMemoryRepository


class MemoryRepository(AbstractMemoryRepository):
    """SQLAlchemy-backed implementation of `AbstractMemoryRepository`."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, memory: Memory) -> Memory:
        self._session.add(memory)
        await self._session.flush()
        await self._session.refresh(memory)
        return memory

    async def get_by_id(
        self, memory_id: uuid.UUID, user_id: uuid.UUID
    ) -> Optional[Memory]:
        stmt = select(Memory).where(
            Memory.id == memory_id,
            Memory.user_id == user_id,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_user(
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
    ) -> Sequence[Memory]:
        stmt = select(Memory).where(Memory.user_id == user_id)

        if memory_type is not None:
            stmt = stmt.where(Memory.memory_type == memory_type)
        if is_pinned is not None:
            stmt = stmt.where(Memory.is_pinned == is_pinned)
        if is_archived is not None:
            stmt = stmt.where(Memory.is_archived == is_archived)
        if min_importance is not None:
            stmt = stmt.where(Memory.importance_score >= min_importance)
        if tags:
            # JSONB containment: memories.tags @> '["tag1","tag2"]'
            stmt = stmt.where(Memory.tags.contains(list(tags)))

        stmt = (
            stmt.order_by(Memory.importance_score.desc(), Memory.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def update(
        self, memory_id: uuid.UUID, user_id: uuid.UUID, values: dict
    ) -> Optional[Memory]:
        if not values:
            return await self.get_by_id(memory_id, user_id)

        stmt = (
            sa_update(Memory)
            .where(Memory.id == memory_id, Memory.user_id == user_id)
            .values(**values)
            .returning(Memory)
        )
        result = await self._session.execute(stmt)
        updated = result.scalar_one_or_none()
        if updated is not None:
            await self._session.flush()
        return updated

    async def delete(self, memory_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        memory = await self.get_by_id(memory_id, user_id)
        if memory is None:
            return False
        await self._session.delete(memory)
        await self._session.flush()
        return True

    async def record_access(
        self, memory_id: uuid.UUID, user_id: uuid.UUID
    ) -> Optional[Memory]:
        stmt = (
            sa_update(Memory)
            .where(Memory.id == memory_id, Memory.user_id == user_id)
            .values(
                access_count=Memory.access_count + 1,
                last_accessed=datetime.now(timezone.utc),
            )
            .returning(Memory)
        )
        result = await self._session.execute(stmt)
        updated = result.scalar_one_or_none()
        if updated is not None:
            await self._session.flush()
        return updated

    async def count_by_user(
        self,
        user_id: uuid.UUID,
        *,
        memory_type: Optional[MemoryType] = None,
        is_archived: Optional[bool] = None,
    ) -> int:
        stmt = select(func.count()).select_from(Memory).where(
            Memory.user_id == user_id
        )
        if memory_type is not None:
            stmt = stmt.where(Memory.memory_type == memory_type)
        if is_archived is not None:
            stmt = stmt.where(Memory.is_archived == is_archived)

        result = await self._session.execute(stmt)
        return result.scalar_one()