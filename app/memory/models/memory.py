"""
Core `Memory` ORM model for the AURA Memory Engine.

This is the single source of truth for how a unit of memory is persisted.
Vector embeddings themselves are NOT stored in this table — they live in
the vector store (see memory/vector/) and are referenced here only by
`embedding_id`, keeping the relational store lean and the vector store
swappable.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum as SqlEnum,
    Float,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.memory.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.memory.models.enums import MemoryType


class Memory(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """
    Represents a single durable, queryable unit of memory belonging to a user.
    """

    __tablename__ = "memories"

    # --- Ownership -------------------------------------------------------
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        comment="Owning user's identifier. Enforced at the service layer; "
        "no FK is declared here to keep the Memory Engine decoupled "
        "from the identity/auth module.",
    )

    # --- Classification ----------------------------------------------------
    memory_type: Mapped[MemoryType] = mapped_column(
        SqlEnum(
            MemoryType,
            name="memory_type_enum",
            native_enum=True,
            validate_strings=True,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
    )

    # --- Content -------------------------------------------------------
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # NOTE: mapped to attribute `metadata_` because `metadata` is reserved
    # on the Declarative Base (`Base.metadata`). The underlying column is
    # still literally named "metadata".
    metadata_: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSONB,
        nullable=False,
        server_default="{}",
        default=dict,
    )

    # --- Scoring -------------------------------------------------------
    importance_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        server_default="0.5",
        default=0.5,
        comment="Normalized 0.0-1.0 salience score used for retrieval ranking.",
    )

    confidence_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        server_default="1.0",
        default=1.0,
        comment="Normalized 0.0-1.0 confidence that this memory is accurate.",
    )

    # --- Vector linkage --------------------------------------------------
    embedding_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Foreign reference into the external vector store (memory/vector/).",
    )

    source: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Origin of the memory, e.g. 'conversation', 'integration:calendar'.",
    )

    tags: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
        server_default="[]",
        default=list,
    )

    # --- Lifecycle / usage flags ----------------------------------------
    is_pinned: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false", default=False
    )

    is_archived: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false", default=False
    )

    access_count: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0", default=0
    )

    last_accessed: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            "importance_score >= 0.0 AND importance_score <= 1.0",
            name="ck_memories_importance_score_range",
        ),
        CheckConstraint(
            "confidence_score >= 0.0 AND confidence_score <= 1.0",
            name="ck_memories_confidence_score_range",
        ),
        CheckConstraint(
            "access_count >= 0",
            name="ck_memories_access_count_non_negative",
        ),
        Index("ix_memories_user_id", "user_id"),
        Index("ix_memories_memory_type", "memory_type"),
        Index("ix_memories_created_at", "created_at"),
        Index("ix_memories_importance_score", "importance_score"),
        Index("ix_memories_last_accessed", "last_accessed"),
        Index("ix_memories_embedding_id", "embedding_id"),
        Index("ix_memories_user_id_memory_type", "user_id", "memory_type"),
    )

    def __repr__(self) -> str:
        return (
            f"<Memory id={self.id} user_id={self.user_id} "
            f"type={self.memory_type.value} pinned={self.is_pinned} "
            f"archived={self.is_archived}>"
        )