"""
SQLAlchemy model for persisted embeddings, backing the vector store.

Kept separate from `memory/models/memory.py` on purpose: the relational
`Memory` row is small and hot (read on every retrieval), while embedding
vectors are large and read only during similarity search. Splitting them
into their own table avoids bloating the primary `memories` table and
lets this table be indexed with pgvector-specific index types (ivfflat/
hnsw) without affecting the main table's index strategy.
"""
from __future__ import annotations

import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.memory.models.base import Base, UUIDPrimaryKeyMixin
from app.memory.vector.schemas import DEFAULT_EMBEDDING_DIMENSIONS


class MemoryEmbedding(UUIDPrimaryKeyMixin, Base):
    """
    Stores the vector embedding for exactly one `Memory` row.

    `memory_id` carries a real foreign key here (unlike `Memory.user_id`,
    which deliberately has none) because both tables live inside the same
    Memory Engine bounded context and must stay referentially consistent;
    deleting a memory should cascade-delete its embedding.
    """

    __tablename__ = "memory_embeddings"

    memory_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("memories.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        comment="Denormalized from Memory for query-time filtering without a join.",
    )

    model_name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        comment="Identifier of the embedding model that produced this vector, "
        "e.g. 'text-embedding-3-small'.",
    )

    dimensions: Mapped[int] = mapped_column(nullable=False)

    vector: Mapped[list[float]] = mapped_column(
        Vector(DEFAULT_EMBEDDING_DIMENSIONS),
        nullable=False,
    )

    __table_args__ = (
        Index("ix_memory_embeddings_user_id", "user_id"),
        Index("ix_memory_embeddings_memory_id", "memory_id"),
        Index(
            "ix_memory_embeddings_vector_cosine",
            "vector",
            postgresql_using="ivfflat",
            postgresql_with={"lists": 100},
            postgresql_ops={"vector": "vector_cosine_ops"},
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<MemoryEmbedding id={self.id} memory_id={self.memory_id} "
            f"model={self.model_name} dims={self.dimensions}>"
        )