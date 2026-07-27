"""
Domain-level exceptions for the vector store integration layer.
"""
from __future__ import annotations

import uuid


class VectorStoreError(Exception):
    """Base class for all vector store errors."""


class EmbeddingNotFoundError(VectorStoreError):
    """Raised when an embedding cannot be located by id or by memory_id."""

    def __init__(self, identifier: uuid.UUID) -> None:
        self.identifier = identifier
        super().__init__(f"Embedding not found for identifier: {identifier}")


class VectorDimensionMismatchError(VectorStoreError):
    """Raised when a supplied vector's dimensionality does not match the store's configuration."""

    def __init__(self, expected: int, received: int) -> None:
        self.expected = expected
        self.received = received
        super().__init__(
            f"Vector dimension mismatch: expected {expected}, received {received}."
        )