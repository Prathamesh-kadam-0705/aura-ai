"""
Pure scoring/ranking functions for the retrieval engine.

Deliberately free of any I/O (no DB session, no vector store, no
repository) so this module can be exhaustively unit-tested with plain
floats and datetimes.
"""
from __future__ import annotations

import math
from datetime import datetime, timezone

from app.memory.engine.config import RetrievalConfig


def similarity_from_distance(cosine_distance: float) -> float:
    """
    Convert a pgvector cosine distance (range 0.0-2.0, lower = closer)
    into a similarity score in the range 0.0-1.0 (higher = closer).

    Cosine distance is defined as `1 - cosine_similarity`, so similarity
    is recovered as `1 - distance`, then clamped to guard against
    floating-point drift pushing it slightly outside [0.0, 1.0].
    """
    similarity = 1.0 - cosine_distance
    return max(0.0, min(1.0, similarity))


def recency_score(
    reference_time: datetime,
    *,
    now: datetime | None = None,
    half_life_days: float,
) -> float:
    """
    Exponential decay score in (0.0, 1.0], where 1.0 means "just now"
    and the score halves every `half_life_days`.

    Exponential decay (rather than linear) is used so very recent
    memories are sharply favored while old memories asymptotically
    approach zero rather than going negative or requiring clamping.
    """
    current_time = now or datetime.now(timezone.utc)
    if reference_time.tzinfo is None:
        reference_time = reference_time.replace(tzinfo=timezone.utc)

    elapsed_days = max(0.0, (current_time - reference_time).total_seconds() / 86400.0)
    decay_constant = math.log(2) / half_life_days
    return math.exp(-decay_constant * elapsed_days)


def compute_final_score(
    *,
    similarity: float,
    importance: float,
    recency: float,
    is_pinned: bool,
    config: RetrievalConfig,
) -> float:
    """
    Combine the three weighted signals into a single ranking score,
    then apply a flat additive boost for pinned memories.

    Weighted linear combination (rather than a learned model) is used
    deliberately: it is transparent, requires no training data, and
    every term's contribution is auditable by a human operator.
    """
    weighted_score = (
        similarity * config.similarity_weight
        + importance * config.importance_weight
        + recency * config.recency_weight
    )
    if is_pinned:
        weighted_score += config.pin_boost
    return weighted_score