"""
The Retrieval Engine: the reasoning core of the Memory Engine.

Orchestrates a hybrid retrieval pipeline:
  1. Similarity search against the vector store for a candidate pool.
  2. Hydration of full memory rows via the relational repository.
  3. Hybrid re-ranking (similarity + importance + recency + pin boost).
  4. Optional access-tracking side effect on the returned memories.

This class depends only on abstractions (`AbstractVectorStore`,
`AbstractMemoryRepository`) — never on `PgVectorStore` or
`MemoryRepository` concretely — so it remains fully testable with fakes
and swappable at the infrastructure layer.
"""
from __future__ import annotations

from app.memory.engine.config import DEFAULT_RETRIEVAL_CONFIG, RetrievalConfig
from app.memory.engine.exceptions import InvalidRetrievalRequestError
from app.memory.engine.ranking import (
    compute_final_score,
    recency_score,
    similarity_from_distance,
)
from app.memory.engine.schemas import RankedMemory, RetrievalRequest, RetrievalResult
from app.memory.models.memory import Memory
from app.memory.repositories.base import AbstractMemoryRepository
from app.memory.schemas.memory import MemorySummary
from app.memory.vector.base import AbstractVectorStore
from app.memory.vector.schemas import VectorQueryRequest


class RetrievalEngine:
    """Hybrid similarity + salience retrieval over a user's memories."""

    def __init__(
        self,
        vector_store: AbstractVectorStore,
        memory_repository: AbstractMemoryRepository,
        *,
        config: RetrievalConfig = DEFAULT_RETRIEVAL_CONFIG,
    ) -> None:
        self._vector_store = vector_store
        self._memory_repository = memory_repository
        self._config = config

    async def retrieve(self, request: RetrievalRequest) -> RetrievalResult:
        if request.top_k < 1:
            raise InvalidRetrievalRequestError("top_k must be at least 1.")

        candidate_pool_size = request.top_k * self._config.candidate_pool_multiplier

        vector_query = VectorQueryRequest(
            user_id=request.user_id,
            query_vector=request.query_vector,
            top_k=candidate_pool_size,
        )
        vector_hits = await self._vector_store.query(vector_query)

        if not vector_hits:
            return RetrievalResult(
                user_id=request.user_id,
                results=[],
                total_candidates_considered=0,
            )

        distance_by_memory_id = {hit.memory_id: hit.distance for hit in vector_hits}

        hydrated: list[Memory] = []
        for hit in vector_hits:
            memory = await self._memory_repository.get_by_id(
                hit.memory_id, request.user_id
            )
            if memory is None:
                # Embedding row survived a memory deletion race, or belongs
                # to a memory type filtered out below — skip, don't fail.
                continue
            if self._config.exclude_archived and memory.is_archived:
                continue
            if request.memory_type is not None and memory.memory_type != request.memory_type:
                continue
            hydrated.append(memory)

        ranked: list[RankedMemory] = []
        for memory in hydrated:
            distance = distance_by_memory_id[memory.id]
            similarity = similarity_from_distance(distance)
            recency = recency_score(
                memory.last_accessed or memory.created_at,
                half_life_days=self._config.recency_half_life_days,
            )
            final_score = compute_final_score(
                similarity=similarity,
                importance=memory.importance_score,
                recency=recency,
                is_pinned=memory.is_pinned,
                config=self._config,
            )
            ranked.append(
                RankedMemory(
                    memory=MemorySummary.model_validate(memory),
                    similarity_score=similarity,
                    recency_score=recency,
                    final_score=final_score,
                )
            )

        ranked.sort(key=lambda item: item.final_score, reverse=True)
        top_results = ranked[: request.top_k]

        if request.record_access:
            for result in top_results:
                await self._memory_repository.record_access(
                    result.memory.id, request.user_id
                )

        return RetrievalResult(
            user_id=request.user_id,
            results=top_results,
            total_candidates_considered=len(hydrated),
        )