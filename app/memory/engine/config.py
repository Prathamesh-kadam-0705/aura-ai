"""
Tunable configuration for the retrieval engine's hybrid ranking strategy.

Kept as an explicit, injectable dataclass rather than module-level
constants so different callers (e.g. a "quick recall" surface vs. a
"deep reflection" surface) can supply different weighting profiles
without subclassing or monkeypatching the engine.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetrievalConfig:
    """
    Weights and knobs controlling how candidate memories are scored.

    All `*_weight` fields should sum to roughly 1.0 for the final score
    to stay in a predictable 0.0-1.0-ish range, though this is not
    enforced — callers may intentionally overweight one signal.
    """

    similarity_weight: float = 0.55
    importance_weight: float = 0.25
    recency_weight: float = 0.15
    pin_boost: float = 0.05
    """Flat additive bonus applied to pinned memories after weighted scoring."""

    recency_half_life_days: float = 30.0
    """Number of days after which a memory's recency contribution halves."""

    candidate_pool_multiplier: int = 3
    """
    How many extra candidates to pull from the vector store beyond the
    caller's requested `top_k`, so post-filtering (archived exclusion,
    re-ranking) still leaves enough results.
    """

    exclude_archived: bool = True


DEFAULT_RETRIEVAL_CONFIG = RetrievalConfig()