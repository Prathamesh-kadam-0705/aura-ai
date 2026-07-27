"""
pgvector-backed implementation of `AbstractVectorStore`.

Uses PostgreSQL's `vector` extension via the `pgvector` Python package's
SQLAlchemy integration. Similarity is computed with cosine distance
(`<=>` operator, exposed here through `Vector.cosine_distance`), matched
to the `vector_cosine_ops` index defined on `MemoryEmbedding.vector`.
"""
from __future__ import annotations

import uuid
from typing import Optional, Sequence

from sqlalchemy import delete as sa_delete, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.memory.vector.base import AbstractVectorStore
from app.memory.vector.exceptions import VectorDimensionMismatchError
from app.memory.vector.models import MemoryEmbedding
from app.memory.vector.schemas import (
    DEFAULT_EMBEDDING_DIMENSIONS,
    VectorQueryRequest,
    VectorRecordRead,
    VectorSearchResult,
    VectorUpsertRequest,
)


class PgVectorStore(AbstractVectorStore):
    """Concrete vector store backed by a PostgreSQL `vector` column."""

    def __init__(
        self,
        session: AsyncSession,
        *,
        dimensions: int = DEFAULT_EMBEDDING_DIMENSIONS,
    ) -> None:
        self._session = session
        self._dimensions = dimensions

    def _validate_dimensions(self, vector: list[float]) -> None:
        if len(vector) != self._dimensions:
            raise VectorDimensionMismatchError(
                expected=self._dimensions, received=len(vector)
            )

    async def upsert(self, request: VectorUpsertRequest) -> VectorRecordRead:
        self._validate_dimensions(request.vector)

        stmt = (
            pg_insert(MemoryEmbedding)
            .values(
                memory_id=request.memory_id,
                user_id=request.user_id,
                model_name=request.model_name,
                dimensions=self._dimensions,
                vector=request.vector,
            )
            .on_conflict_do_update(
                index_elements=[MemoryEmbedding.memory_id],
                set_={
                    "model_name": request.model_name,
                    "dimensions": self._dimensions,
                    "vector": request.vector,
                },
            )
            .returning(MemoryEmbedding)
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one()
        await self._session.flush()
        return VectorRecordRead.model_validate(row)

    async def query(
        self, request: VectorQueryRequest
    ) -> Sequence[VectorSearchResult]:
        self._validate_dimensions(request.query_vector)

        distance_expr = MemoryEmbedding.vector.cosine_distance(
            request.query_vector
        ).label("distance")

        stmt = (
            select(
                MemoryEmbedding.id,
                MemoryEmbedding.memory_id,
                distance_expr,
            )
            .where(MemoryEmbedding.user_id == request.user_id)
            .order_by(distance_expr.asc())
            .limit(request.top_k)
        )

        if request.max_distance is not None:
            stmt = stmt.where(distance_expr <= request.max_distance)

        result = await self._session.execute(stmt)
        rows = result.all()

        return [
            VectorSearchResult(
                embedding_id=row.id,
                memory_id=row.memory_id,
                distance=float(row.distance),
            )
            for row in rows
        ]

    async def get_by_memory_id(
        self, memory_id: uuid.UUID, user_id: uuid.UUID
    ) -> Optional[VectorRecordRead]:
        stmt = select(MemoryEmbedding).where(
            MemoryEmbedding.memory_id == memory_id,
            MemoryEmbedding.user_id == user_id,
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        return VectorRecordRead.model_validate(row) if row is not None else None

    async def delete_by_memory_id(
        self, memory_id: uuid.UUID, user_id: uuid.UUID
    ) -> bool:
        stmt = (
            sa_delete(MemoryEmbedding)
            .where(
                MemoryEmbedding.memory_id == memory_id,
                MemoryEmbedding.user_id == user_id,
            )
            .returning(MemoryEmbedding.id)
        )
        result = await self._session.execute(stmt)
        deleted_row = result.first()
        if deleted_row is not None:
            await self._session.flush()
            return True
        return False