"""
Abstract vector store contract for the Memory Engine.

The (not yet generated) Engine layer will depend only on this interface,
never on `PgVectorStore` directly, so the underlying vector backend
(pgvector today; potentially Pinecone/Qdrant/Weaviate later) can be
swapped without touching retrieval logic.
"""
from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import Optional, Sequence

from app.memory.vector.schemas import (
    VectorQueryRequest,
    VectorRecordRead,
    VectorSearchResult,
    VectorUpsertRequest,
)


class AbstractVectorStore(ABC):
    """Persistence and similarity-search contract for memory embeddings."""

    @abstractmethod
    async def upsert(self, request: VectorUpsertRequest) -> VectorRecordRead:
        """Create or replace the embedding associated with `request.memory_id`."""
        raise NotImplementedError

    @abstractmethod
    async def query(
        self, request: VectorQueryRequest
    ) -> Sequence[VectorSearchResult]:
        """Return the `top_k` nearest embeddings for a user, ranked by distance."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_memory_id(
        self, memory_id: uuid.UUID, user_id: uuid.UUID
    ) -> Optional[VectorRecordRead]:
        """Fetch the embedding record for a given memory, if one exists."""
        raise NotImplementedError

    @abstractmethod
    async def delete_by_memory_id(
        self, memory_id: uuid.UUID, user_id: uuid.UUID
    ) -> bool:
        """Delete the embedding associated with a memory. Returns True if removed."""
        raise NotImplementedError