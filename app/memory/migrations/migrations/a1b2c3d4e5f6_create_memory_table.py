"""create memory table

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2026-07-23 00:00:00.000000
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


MEMORY_TYPE_ENUM_NAME = "memory_type_enum"
MEMORY_TYPE_VALUES = (
    "SHORT_TERM",
    "LONG_TERM",
    "PREFERENCE",
    "FACT",
    "EVENT",
    "PROJECT",
    "GOAL",
    "TASK",
    "RELATIONSHIP",
    "HABIT",
    "KNOWLEDGE",
    "CONVERSATION",
)


def upgrade() -> None:
    # Required for gen_random_uuid() used as the server-side PK default.
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    memory_type_enum = postgresql.ENUM(
        *MEMORY_TYPE_VALUES,
        name=MEMORY_TYPE_ENUM_NAME,
    )
    memory_type_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "memories",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "memory_type",
            memory_type_enum,
            nullable=False,
        ),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column(
            "metadata",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "importance_score",
            sa.Float(),
            server_default=sa.text("0.5"),
            nullable=False,
        ),
        sa.Column(
            "confidence_score",
            sa.Float(),
            server_default=sa.text("1.0"),
            nullable=False,
        ),
        sa.Column("embedding_id", sa.String(length=255), nullable=True),
        sa.Column("source", sa.String(length=255), nullable=True),
        sa.Column(
            "tags",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "is_pinned",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "is_archived",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "access_count",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column("last_accessed", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="pk_memories"),
        sa.CheckConstraint(
            "importance_score >= 0.0 AND importance_score <= 1.0",
            name="ck_memories_importance_score_range",
        ),
        sa.CheckConstraint(
            "confidence_score >= 0.0 AND confidence_score <= 1.0",
            name="ck_memories_confidence_score_range",
        ),
        sa.CheckConstraint(
            "access_count >= 0",
            name="ck_memories_access_count_non_negative",
        ),
    )

    op.create_index("ix_memories_user_id", "memories", ["user_id"])
    op.create_index("ix_memories_memory_type", "memories", ["memory_type"])
    op.create_index("ix_memories_created_at", "memories", ["created_at"])
    op.create_index("ix_memories_importance_score", "memories", ["importance_score"])
    op.create_index("ix_memories_last_accessed", "memories", ["last_accessed"])
    op.create_index("ix_memories_embedding_id", "memories", ["embedding_id"])
    op.create_index(
        "ix_memories_user_id_memory_type",
        "memories",
        ["user_id", "memory_type"],
    )


def downgrade() -> None:
    op.drop_index("ix_memories_user_id_memory_type", table_name="memories")
    op.drop_index("ix_memories_embedding_id", table_name="memories")
    op.drop_index("ix_memories_last_accessed", table_name="memories")
    op.drop_index("ix_memories_importance_score", table_name="memories")
    op.drop_index("ix_memories_created_at", table_name="memories")
    op.drop_index("ix_memories_memory_type", table_name="memories")
    op.drop_index("ix_memories_user_id", table_name="memories")

    op.drop_table("memories")

    postgresql.ENUM(name=MEMORY_TYPE_ENUM_NAME).drop(op.get_bind(), checkfirst=True)