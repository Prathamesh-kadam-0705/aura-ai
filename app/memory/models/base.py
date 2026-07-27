"""
Base declarative class and shared mixins for the Memory Engine ORM models.

This module intentionally contains no domain logic. It exists purely to
provide the declarative base and reusable column mixins (primary key,
timestamps) so every model in the engine shares identical, predictable
column semantics.
"""
from __future__ import annotations

import uuid

from datetime import datetime

from sqlalchemy import DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Shared declarative base for all Memory Engine ORM models."""


class UUIDPrimaryKeyMixin:
    """
    Provides a UUID v4 primary key.

    The default is generated client-side by SQLAlchemy (`uuid.uuid4`) so the
    ORM object has a usable `id` immediately after instantiation, and is
    mirrored server-side via `gen_random_uuid()` (pgcrypto) so the column is
    also safe for raw SQL inserts issued outside the ORM.
    """

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        nullable=False,
    )


class TimestampMixin:
    """
    Provides timezone-aware `created_at` / `updated_at` columns.

    `created_at` is stamped once at insert time via a server-side default.
    `updated_at` is stamped at insert time and re-stamped on every UPDATE
    via SQLAlchemy's `onupdate`, so callers never need to set it manually.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now()"),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now()"),
        onupdate=text("now()"),
        nullable=False,
    )