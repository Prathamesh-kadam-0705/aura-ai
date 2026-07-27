"""
Public exports for the Memory Engine's vector store integration layer.
"""
from app.memory.vector.base import AbstractVectorStore
from app.memory.vector.exceptions import (
    EmbeddingNotFoundError,
    VectorDimensionMismatchError,
    VectorStoreError,
)
from app.memory.vector.models import MemoryEmbedding
from app.memory.vector.pgvector_store import PgVectorStore
from app.memory.vector.schemas import (
    DEFAULT_EMBEDDING_DIMENSIONS,
    VectorQueryRequest,
    VectorRecordRead,
    VectorSearchResult,
    VectorUpsertRequest,
)

__all__ = [
    "AbstractVectorStore",
    "PgVectorStore",
    "MemoryEmbedding",
    "VectorStoreError",
    "EmbeddingNotFoundError",
    "VectorDimensionMismatchError",
    "DEFAULT_EMBEDDING_DIMENSIONS",
    "VectorUpsertRequest",
    "VectorQueryRequest",
    "VectorRecordRead",
    "VectorSearchResult",
]