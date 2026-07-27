"""
Abstract repository contract for the Memory Engine.

Defining this as an ABC (rather than relying on structural typing alone)
gives the service layer (not yet generated) a single, explicit
dependency to type-hint against, and makes it possible to substitute a
fake/in-memory repository in tests without touching consumer code.
"""
from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import Optional, Sequence

from app.memory.models.enums import MemoryType
from app.memory.models.memory import Memory


class AbstractMemoryRepository(ABC):
    """Persistence contract for `Memory` entities."""

    @abstractmethod
    async def create(self, memory: Memory) -> Memory:
        """Persist a new `Memory` instance and return it, refreshed from the DB."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self, memory_id: uuid.UUID, user_id: uuid.UUID
    ) -> Optional[Memory]:
        """
        Fetch a single memory by id, scoped to `user_id`.

        Scoping by `user_id` at the query level (not just the caller's
        responsibility) prevents cross-tenant data leakage even if a
        higher layer forgets to check ownership.
        """
        raise NotImplementedError

    @abstractmethod
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
        """List memories for a user with optional filters, paginated."""
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, memory_id: uuid.UUID, user_id: uuid.UUID, values: dict
    ) -> Optional[Memory]:
        """Apply a partial update to a memory. Returns None if not found."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, memory_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        """Hard-delete a memory. Returns True if a row was removed."""
        raise NotImplementedError

    @abstractmethod
    async def record_access(
        self, memory_id: uuid.UUID, user_id: uuid.UUID
    ) -> Optional[Memory]:
        """Increment `access_count` and stamp `last_accessed` for a memory."""
        raise NotImplementedError

    @abstractmethod
    async def count_by_user(
        self,
        user_id: uuid.UUID,
        *,
        memory_type: Optional[MemoryType] = None,
        is_archived: Optional[bool] = None,
    ) -> int:
        """Count memories for a user with optional filters."""
        raise NotImplementedError