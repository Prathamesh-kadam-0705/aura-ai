"""
Domain-level exceptions for the Memory Engine service layer.

These are transport-agnostic on purpose: this module has no knowledge of
FastAPI/HTTP status codes. Translating a `MemoryNotFoundError` into a 404,
for example, is the responsibility of the (not yet generated) API layer.
"""
from __future__ import annotations

import uuid


class MemoryServiceError(Exception):
    """Base class for all Memory Engine service-layer errors."""


class MemoryNotFoundError(MemoryServiceError):
    """Raised when a memory does not exist or is not owned by the requesting user."""

    def __init__(self, memory_id: uuid.UUID, user_id: uuid.UUID) -> None:
        self.memory_id = memory_id
        self.user_id = user_id
        super().__init__(
            f"Memory {memory_id} not found for user {user_id}."
        )


class MemoryValidationError(MemoryServiceError):
    """Raised when a business rule (not a schema-level rule) is violated."""


class MemoryOperationNotAllowedError(MemoryServiceError):
    """Raised when a requested state transition is not permitted."""